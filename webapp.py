import streamlit as st
import pandas as pd
import re
import sqlite3



conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


def set_bg_hack_url():
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://i.ibb.co/pwVPLh9/BK.jpg");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()
st.title("Welcome To Justice")


menu = ["Home","SignUp","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.markdown(
    """
    <p align="justify">
    <b style="color:black">AI Legal is an AI-based approach that utilizes case descriptions in order to predict law section classifications based on K-Nearest Neighbors (KNN), Linear Support Vector Machine (SVM), Decision Tree, Random Forest and Extra Trees Classifier. These models were chosen because of their advantage in dealing with large quantities of legal data and diverse feature interdependencies. In classification based on proximity, we have KNN while for the linear decision boundaries, Linear SVM is the best model. Decision Trees are easy to interpret, and Random Forest reduces variance and produces more accurate results. But Extra Trees Classifier yields the highest accuracy and training speed as well as less prone to overfitting.</b>
    </p>
    """
    ,unsafe_allow_html=True)
    
elif choice == "SignUp":
    FirstName = st.text_input("Firstname")
    LastName = st.text_input("Lastname")
    Mobile = st.text_input("Mobile")
    City = st.text_input("City")
    Email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    Cpassword = st.text_input("Confirm Password",type='password')
    if st.button("Signup"):
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (pattern.match(Mobile)):
            if re.fullmatch(regex, Email):
                create_usertable()
                add_userdata(FirstName,LastName,Mobile,City,Email,new_password,Cpassword)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
            else:
                 st.warning("Not Valid Email")
        else:
             st.warning("Not Valid Mobile Number")
             
elif choice == "Login":
    st.subheader("Login Section")
    Email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password",type='password')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if st.sidebar.checkbox("Login"):
        if re.fullmatch(regex, Email):
            if Email=="a@a.com" and password=="123":
                st.success("Welcome to Admin")
                create_usertable()
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
                
            else:
                
                result = login_user(Email,password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    texts=str(st.text_input("Enter Case Study"))
                
                    names = ["K-Nearest Neighbors", "Liner SVM",
                             "Decision Tree", "Random Forest",
                             "ExtraTreesClassifier"]
                    classifier=st.selectbox("Select ML",names)                  

                    st.button('Predict Section')
                        
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
            
