from typing import Optional
import gradio

# from facefusion import metadata, wording
# import about.css 


ABOUT_BUTTON : Optional[gradio.HTML] = None
DONATE_BUTTON : Optional[gradio.HTML] = None


def render() -> None:
	global ABOUT_BUTTON
	global DONATE_BUTTON

	ABOUT_BUTTON = gradio.Button(
		value='Blue OC',
		variant='primary',
  		elem_classes='blueoc-btn',
		# link=metadata.get('url')
	)
	# DONATE_BUTTON = gradio.Button(
	# 	value = wording.get('uis.donate_button'),
	# 	link = 'https://donate.facefusion.io',
	# 	size = 'sm'
	# )
