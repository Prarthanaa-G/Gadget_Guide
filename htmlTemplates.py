css = '''
<style>

        
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #49357f;
}
.chat-message.bot {
    background-color: #1f1241;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding-right: 10px;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    margin-top: 1rem;
    margin-bottom: 1rem;

}


'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/free-photo/close-up-portrait-smiling-young-woman-looking-camera_171337-17994.jpg?semt=ais_hybrid&w=740">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''