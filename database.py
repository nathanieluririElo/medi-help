import streamlit as st

def db_login_signup(proceed, user_name, password, first_name='None', last_name='None', learning_rate='None', understanding_rate='None'):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MONGO_URI = os.getenv('MONGO_URI')

    connect(MONGO_URI)

    class User(MongoModel):
        user_name = fields.CharField(mongo_name="User Name")
        first_name = fields.CharField(mongo_name="First Name")
        last_name = fields.CharField(mongo_name="Last Name") 
        password = fields.CharField(mongo_name="Password")
        learning_rate = fields.CharField(mongo_name="Learning Speed")
        understanding_rate = fields.CharField(mongo_name="Understanding Speed")


    def signup(user, passw, first_name=None, last_name=None, learning_rate=None, understanding_rate=None):
        hashed_passw = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
        new_user = User(user_name=user, password=hashed_passw, first_name=first_name, last_name=last_name, learning_rate=learning_rate, understanding_rate=understanding_rate)
        if first_name !='None' and last_name!='None' and learning_rate !='None' and understanding_rate !='None':
            new_user.save()
        return new_user

    def login(user, passw):
        users = User.objects.all()

        for u in users:
            if user == u.user_name:
                print(f"{user} and {u.user_name}")
                checkP = u.password
                checkP = checkP[2:-1]
                checkP = bytes(checkP, 'utf-8')
                if bcrypt.checkpw(passw.encode('utf-8'), checkP):
                    print('Login successful')
                    return u

        return None

    def check(user_name: str) -> bool:
        users = User.objects.all()
        if users.count() == 0:
            return True
        else:
            for user in users:
                if user_name == user.user_name:
                    # User name found in the database
                    return False
            # User name not found in the database
            return True
    def start(process, user_name, password, first_name=None, last_name=None, learning_rate=None, understanding_rate=None):
        if process == 1:
            return signup(user_name, password, first_name, last_name, learning_rate, understanding_rate)
        elif process == 2:
            return login(user_name, password)
        
        elif process == 3:
            return check(user_name)
        else:
            raise ValueError("Invalid process")

    return start(proceed, user_name, password, first_name, last_name, learning_rate, understanding_rate)

# db_login_signup(1, "test", "p",first_name="Test",last_name="Test",learning_rate="2",understanding_rate="4")

# print(db_login_signup(2, "test user", "password"))







from bson import ObjectId



@st.cache_resource
def save_history(_UserDetails:ObjectId,AINOTE:list,QUESTIONS:list,QUESTIONSWITHCONTEXT:list):
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MONGO_URI = os.getenv('MONGO_URI')

    connect(MONGO_URI)
    
    class User(MongoModel):
        user_name = fields.CharField(mongo_name="User Name")
        first_name = fields.CharField(mongo_name="First Name")
        last_name = fields.CharField(mongo_name="Last Name") 
        password = fields.CharField(mongo_name="Password")
        learning_rate = fields.CharField(mongo_name="Learning Speed")
        understanding_rate = fields.CharField(mongo_name="Understanding Speed")
    class History(MongoModel):
        UserDetails = fields.ReferenceField(User,mongo_name="User Details")
        AiNote = fields.ListField(mongo_name="AI Generated Note")
        Questions = fields.ListField(mongo_name="AI Generated Questions")
        QuestionsWithContext = fields.ListField(mongo_name="Questions - Context")

    def save(_UserDetails,AINOTE:list,QUESTIONS:list,QUESTIONSWITHCONTEXT:list):

        try:
            new_history = History(UserDetails=_UserDetails,AiNote =AINOTE,Questions=QUESTIONS,QuestionsWithContext=QUESTIONSWITHCONTEXT)
            new_history.save()
            print("Saved")
            return new_history
        except Exception as e:
            return f"Couldn't save because {e}"


    return save(_UserDetails,AINOTE,QUESTIONS,QUESTIONSWITHCONTEXT)



















def history_ID_query(user_id:ObjectId)->list:
    """

    This  function is used to get the list history id's of a user
    to know all the notes a user has saved

    """
    history_ids =[]
    from pymongo import MongoClient
    with MongoClient('localhost',27017) as client:
        db = client['studybotdb']
        collection = db['history']
        query = {"User Details": user_id}
        result = collection.find(query)
        try:
            for document in result:
                history_ids.append(document['_id'])
        except Exception as e:
            return  [f"Error occurred while fetching data :{e}"]


        return history_ids
    










def history_query(history_id: ObjectId) -> list:
    """
    This function is used to get the history of a user
    it returns a list of documents/history
    starting with 0= Ai Note, 1= Ai generated Questions
    2= Questions- context
    it only makes a return for a specific history id
    """
    aigenquestions = []
    ainote=[]
    questionsiwithcontext=[]
    documents=[]

    from pymongo import MongoClient
    with MongoClient('localhost', 27017) as client:
        db = client['studybotdb']
        collection = db['history']
        query = {"_id": history_id}
        result = collection.find(query)
        for document in result:
            aigenquestions.append(document['AI Generated Questions'])
            ainote.append(document['AI Generated Note'])
            questionsiwithcontext.append(document['Questions - Context'])
        documents = [ainote,aigenquestions,questionsiwithcontext]
    return documents

        

def Chathistory_query(history_id: ObjectId) -> list:
    """
    This function is used to get the chat history of a user
    it returns a the history that should be passed into the st.session_state.messages variable

    it only makes a return for a specific history id
    """
    chat_history=[]

    from pymongo import MongoClient
    with MongoClient('localhost', 27017) as client:
        db = client['studybotdb']
        collection = db['history']
        query = {"_id": history_id}
        result = collection.find(query)
        for document in result:
            chat_history.append(document['Chat History'])
            
        
    return chat_history[0]

def updateChatHistory(historyID,messages):
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['studybotdb']
    history = db['history']
    filter_criteria = {'_id':historyID}
    update_operation = {
    '$set': {
        'Chat History': messages
    }}
    print("History ID",historyID)
    history.update_one(filter_criteria, update_operation)


    





hist=history_ID_query(ObjectId('65cf50098b00473f9f5565f3'))

docs=history_query(hist[1])

title = docs[0][0][0].split('\n')[0]# the firt index chooses which document you want to see between 3 the second index chooses the document itself then the section of the document you want to access is the third index

print(title)
chats =Chathistory_query(hist[1])
print(chats)
















