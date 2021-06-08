import gradio as gr
import matplotlib.pyplot as plt


def outbreak_forecast(r, month, countries, social_distancing):
    # ... run model to forecast outbreak and generate plots
    # ... return plt
    return

def predict(x):

    return str(x*2)

r = gr.inputs.Slider(1, 5)

# gr.Interface(fn=outbreak_forecast,
#     inputs=[r, month, countries, "checkbox"], outputs="plot").launch()
if __name__=='__main__':

    f = gr.Interface(fn=predict,
                inputs=[r],
                outputs="text",
                title='滑动条点击Submit')
    f.launch()