import gradio as gr

def greet(name):
  return "Hello " + name + "!!"

iface = gr.Interface(fn=greet, 
                    inputs="text", 
                    outputs="text",
                    title="meetup!",
                    description="请输入你的名字")
iface.launch(share=True)