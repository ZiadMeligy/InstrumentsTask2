import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split  # Import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder



class ResultWindow(QMainWindow):
    def __init__(self, results):
        super().__init__()
        self.initUI(results)

    def initUI(self, results):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        for i, answer in enumerate(results, start=1):
            question_label = QLabel(f"Question {i}: {'Yes' if answer else 'No'}")
            font = question_label.font()  # Get the current font
            font.setPointSize(16)  # Set the desired font size (16 in this case)
            question_label.setFont(font)  # Apply the new font
            layout.addWidget(question_label)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.close)
        layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)

        self.central_widget.setLayout(layout)
        
        self.setGeometry(1, 1, 1, 1)  

class BlinkSurveyApp(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model  # Store the model as an instance variable
        self.initUI()

    def initUI(self):
        # Load your dataset and train your model here
        # Replace the following lines with your actual data and model
        from scipy.io import arff
        file_path = "EEG Eye State.arff"
        data, meta = arff.loadarff(file_path)

        # Convert the data to a DataFrame
        import pandas as pd
        data = pd.DataFrame(data)
        X = data.drop(columns=['eyeDetection'])
        y = data['eyeDetection']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
        label_encoder = LabelEncoder()
        y_train_encoded = label_encoder.fit_transform(y_train)
        self.model.fit(X_train, y_train_encoded)  # Use self.model to store the model
        self.y_test_predict = self.model.predict(X_test)

        self.questions = [
            "Question 1: Have you encountered accessibility challenges in public spaces in the past month?",
            "Question 2: Do you feel comfortable asking for accommodations when needed?",
            "Question 3: Would you be interested in attending disability-specific workshops or events?",
            "Question 4: Have you faced communication barriers due to your disability recently?",
            "Question 5: Do you have access to assistive technologies that meet your needs?",
            "Question 6: Would you benefit from information on available disability support services in your area?",
            "Question 7: Have you ever experienced discrimination or stigma related to your disability?",
            "Question 8: Would you like to receive updates on accessible events or activities in your community?"
        ]

        self.blink_data = self.y_test_predict  # Initialize with None
        self.blink_data = self.blink_data[:len(self.questions)]
        self.answers = []
        self.current_question = 0

        self.btn_start = QPushButton('Start Test', self)
        self.btn_start.clicked.connect(self.startBlinkSurvey)

        self.lbl_question = QLabel(self)
        self.lbl_question.setText(self.questions[0])
        font = self.lbl_question.font()  # Get the current font
        font.setPointSize(16)  # Set the desired font size (16 in this case)
        self.lbl_question.setFont(font)  # Apply the new font

        self.btn_yes = QPushButton('Yes', self)
        
        font = self.btn_yes.font()  # Get the current font
        font.setPointSize(14)  # Set the desired font size (16 in this case)
        self.btn_yes.setFont(font)  # Apply the new font

        self.btn_no = QPushButton('No', self)
                
        font = self.btn_no.font()  # Get the current font
        font.setPointSize(14)  # Set the desired font size (16 in this case)
        self.btn_no.setFont(font)  # Apply the new font

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_question)
        self.layout.addWidget(self.btn_yes)
        self.layout.addWidget(self.btn_no)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.processBlinkData)

        self.setGeometry(200, 100, 700, 300)
        self.setWindowTitle('Blink Survey App')
        self.show()
        self.result_window = None

    def startBlinkSurvey(self):
        self.current_question = -1  # Initialize to -1 to handle first question
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.processBlinkData)
        self.timer.start(1000) 

    def processBlinkData(self):
        self.current_question += 1

        if self.current_question < len(self.questions):
            if self.blink_data[self.current_question] == 0:
                self.btn_no.setStyleSheet('background-color: green')
                self.btn_yes.setStyleSheet('background-color: none')
            else:
                self.btn_yes.setStyleSheet('background-color: green')
                self.btn_no.setStyleSheet('background-color: none')

            self.lbl_question.setText(self.questions[self.current_question])
        else:
            self.answers_text = "\n".join([f"Question {i+1}: {'Yes' if ans == 1 else 'No'}" for i, ans in enumerate(self.blink_data)])
            self.showResultWindow()  
            # Add this line
            # Generate the answers_text string
            #self.result_window.setPlainText(self.answers_text)

   
    def showResultWindow(self):
        result_window = ResultWindow(self.answers)
        result_window.show()
        self.result_window = QMessageBox()
        self.result_window.setWindowTitle("Thank you, Here is the survey results:")
        self.result_window.setGeometry(100, 100, 600, 400)  # Set the geometry here
        self.result_window.setText(self.answers_text)
        self.result_window.setStandardButtons(QMessageBox.Ok)
        self.result_window.buttonClicked.connect(self.closeResultWindow)
        self.result_window.exec_()
        




    def closeResultWindow(self):
        self.result_window.close()
        self.close()
        print (self.blink_data)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = RandomForestClassifier()  # Initialize your model
    ex = BlinkSurveyApp(model)
    sys.exit(app.exec_())
