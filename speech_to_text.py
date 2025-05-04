import speech_recognition as sr
import pyaudio
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QTextEdit, QLabel, QMessageBox, QHBoxLayout,
                           QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont
import threading
import sys
import queue
import time

class SpeechToTextApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech to Text with Video Recording")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize variables
        self.is_recording = False
        self.video_capture = None
        self.recognizer = sr.Recognizer()
        self.audio_data = []
        self.recording_start_time = 0
        self.generated_text = ""  # Store the generated text
        self.text_history = []    # Store history of all generated texts
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Video display with frame
        video_frame = QFrame()
        video_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        video_frame.setLineWidth(2)
        video_layout = QVBoxLayout(video_frame)
        
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setAlignment(Qt.AlignCenter)
        video_layout.addWidget(self.video_label)
        main_layout.addWidget(video_frame)
        
        # Recording indicator and duration
        status_layout = QHBoxLayout()
        
        self.recording_indicator = QLabel()
        self.recording_indicator.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
        self.recording_indicator.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.recording_indicator)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setStyleSheet("font-size: 14px;")
        self.duration_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(status_layout)
        
        # Text display with frame
        text_frame = QFrame()
        text_frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        text_frame.setLineWidth(2)
        text_layout = QVBoxLayout(text_frame)
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setMinimumHeight(100)
        self.text_display.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        text_layout.addWidget(self.text_display)
        main_layout.addWidget(text_frame)
        
        # Control buttons in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.record_button = QPushButton("Start Recording")
        self.record_button.setFixedWidth(150)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.record_button.clicked.connect(self.toggle_recording)
        button_layout.addWidget(self.record_button)
        
        self.clear_button = QPushButton("Clear Text")
        self.clear_button.setFixedWidth(150)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(self.status_label)
        
        # Initialize video capture
        self.initialize_camera()
        
        # Start video preview
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video)
        self.timer.start(30)  # Update every 30ms
        
        # Timer for recording duration
        self.duration_timer = QTimer()
        self.duration_timer.timeout.connect(self.update_duration)
        self.duration_timer.setInterval(1000)  # Update every second
        
    def initialize_camera(self):
        try:
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                QMessageBox.warning(self, "Camera Error", 
                                  "Could not access the camera. Please check camera permissions in System Preferences > Security & Privacy > Privacy > Camera")
                self.video_capture = None
        except Exception as e:
            QMessageBox.warning(self, "Camera Error", 
                              f"Error initializing camera: {str(e)}")
            self.video_capture = None
        
    def update_video(self):
        if self.video_capture is not None and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                # Convert frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Resize frame to fit the window
                frame = cv2.resize(frame, (640, 480))
                
                # Convert to QImage
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Update video label
                self.video_label.setPixmap(QPixmap.fromImage(qt_image))
            else:
                self.status_label.setText("Error: Could not read from camera")
        else:
            self.status_label.setText("Camera not available")
    
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        self.is_recording = True
        self.record_button.setText("Stop Recording")
        self.status_label.setText("Recording...")
        self.recording_indicator.setText("● RECORDING")
        self.recording_start_time = time.time()
        self.duration_timer.start()
        self.audio_data = []  # Clear previous recording data
        
        # Start speech recognition in a separate thread
        self.recognition_thread = threading.Thread(target=self.record_speech)
        self.recognition_thread.start()
    
    def stop_recording(self):
        self.is_recording = False
        self.record_button.setText("Start Recording")
        self.status_label.setText("Processing audio...")
        self.recording_indicator.setText("")
        self.duration_timer.stop()
        
        # Process all recorded audio
        self.process_recorded_audio()
    
    def update_duration(self):
        if self.is_recording:
            duration = int(time.time() - self.recording_start_time)
            minutes = duration // 60
            seconds = duration % 60
            self.duration_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def record_speech(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                
                while self.is_recording:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        self.audio_data.append(audio)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        self.status_label.setText(f"Error: {str(e)}")
                        break
                    except Exception as e:
                        self.status_label.setText(f"Error: {str(e)}")
                        break
        except Exception as e:
            QMessageBox.warning(self, "Microphone Error", 
                              f"Error accessing microphone: {str(e)}")
            self.stop_recording()
    
    def process_recorded_audio(self):
        try:
            self.status_label.setText("Converting speech to text...")
            current_text = ""  # Temporary variable to store current session's text
            
            for audio in self.audio_data:
                try:
                    text = self.recognizer.recognize_google(audio)
                    current_text += text + " "  # Add space between segments
                    self.update_text(text)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    self.status_label.setText(f"Error: {str(e)}")
                    break
            
            # Store the generated text
            if current_text.strip():  # Only store if there's actual text
                self.generated_text = current_text.strip()
                self.text_history.append(self.generated_text)
            
            self.status_label.setText("Ready")
        except Exception as e:
            self.status_label.setText(f"Error processing audio: {str(e)}")
    
    def update_text(self, text):
        self.text_display.append(text)
    
    def get_generated_text(self):
        """Return the most recently generated text"""
        return self.generated_text
    
    def get_text_history(self):
        """Return the history of all generated texts"""
        return self.text_history
    
    def clear_text(self):
        """Clear both the display and stored text"""
        self.text_display.clear()
        self.generated_text = ""
        self.text_history = []
        self.status_label.setText("Text cleared")
    
    def closeEvent(self, event):
        if self.video_capture is not None:
            self.video_capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec_()) 