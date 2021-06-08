import gradio as gr

def recognize_digit(img):
    # ... implement digit recognition model on input array 
    # ... return dictionary of labels and confidences 

    return

gr.Interface(fn=recognize_digit, inputs="sketchpad", outputs="label").launch()