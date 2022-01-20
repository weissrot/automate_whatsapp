from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://ying:5201314grace@cluster0.76hht.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["whatsapp"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)

@app.route("/", methods=["get","post"])
def reply():
    #getting text
    text = request.form.get("Body")
    #get number
    number = request.form.get("From")
    response = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        response.message("Hi, thanks for contacting *The Cutest Bot*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ talking about *relationship* 😘 \n 2️⃣ talking about *work* 😅 \n 3️⃣ talking about *sports* 😎 \n 4️⃣ "
                    "talking about *happiness* 😀")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)

        if option == 1:
            response.message(
                "You can message me through phone or e-mail.\n\n*Phone*: 991234 56789 \n*E-mail* : contact@theredvelvet.io")
        elif option == 2:
            response.message("You have entered *working mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            response.message(
                "What do you want to talk about?")
        elif option == 3:
            response.message("I do sports from *9 a.m. to 5 p.m*.")
        elif option == 4:
            response.message("your smile lightens my day")
        else:
            response.message("Please enter a valid response")
    elif user["status"] == "ordering":
        if "handsome" in text:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message("Frederik")
        elif "hi" in text
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message("Good morning! What do you plan to do today?")
        else:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message("Let me think about it")

    users.update_one({"number": number}, {"$push": {"messages": {"text": text}}})
    return str(response)

if __name__ == "__main__":
    app.run()

