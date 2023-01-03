import argparse
import pyttsx3
import PyPDF2
from gtts import gTTS

def pdf_to_audio(pdf_file, audio_file, library):
    if library == 'pyttsx3':
        # Initialize the speech engine
        engine = pyttsx3.init()

        # Set the rate of speech
        engine.setProperty('rate', 150)

        # Open the PDF file in read-only mode
        with open(pdf_file, 'rb') as file:
            # Create a PDF object
            pdf = PyPDF2.PdfFileReader(file)

            # Open the audio file in write mode
            with open(audio_file, 'w') as audio:
                # Iterate over each page in the PDF
                for page in range(pdf.getNumPages()):
                    # Extract the text from the page
                    text = pdf.getPage(page).extractText()

                    # Use the speech engine to speak the text
                    engine.say(text)
                    engine.runAndWait()

                    # Write the text to the audio file
                    audio.write(text)
    elif library == 'gTTS':
        # Initialize the text-to-speech engine
        tts = gTTS()

        # Open the PDF file in read-only mode
        with open(pdf_file, 'rb') as file:
            # Create a PDF object
            pdf = PyPDF2.PdfFileReader(file)

            # Iterate over each page in the PDF
            for page in range(pdf.getNumPages()):
                # Extract the text from the page
                text = pdf.getPage(page).extractText()

                # Set the text as the input to the TTS engine
                tts.text = text

                # Save the audio output to the MP3 file
                tts.save(audio_file)

if __name__ == '__main__':
    # Create a parser for the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf_file', help='The PDF file to convert')
    parser.add_argument('audio_file', help='The audio file to create')
    parser.add_argument('--library', choices=['pyttsx3', 'gTTS'], default='pyttsx3',
                        help='The library to use for text-to-speech')
    args = parser.parse_args()

    # Call the pdf_to_audio function with the specified arguments
    pdf_to_audio(args.pdf_file, args.audio_file, args.library)
