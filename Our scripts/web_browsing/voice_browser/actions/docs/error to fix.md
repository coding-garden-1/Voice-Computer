

# Next features:
# COntinuous audio stream pieced together; if the last 1 second was not quiet, assume the person was still talking and save their prompt, eventually piecing together
# clear_numbers() at end of element_clicker()
# decrease fuzzy ratio
# fix a second stale element error with a try except block
"""<pre>Recording audio for 4 seconds. Speak into the microphone...
Audio recording saved to recorded_audio.wav
No number match found. Performing voice dictation instead.
Recording audio for 4 seconds. Speak into the microphone...
Audio recording saved to recorded_audio.wav
Clicked element 12
Traceback (most recent call last):
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 220, in &lt;module&gt;
    numbers_visible = element_clicker(numbers_visible)
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 179, in element_clicker
    print_numbers_on_screen(&quot;nothing&quot;)
  File &quot;/home/rose/Desktop/Projects/Current/Voice Computer/My own scripts/voice_browser.py&quot;, line 106, in print_numbers_on_screen
    driver.execute_script(&quot;arguments[0].innerText += &apos; [{}]&apos;;&quot;.format(i), element)
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py&quot;, line 407, in execute_script
    return self.execute(command, {&quot;script&quot;: script, &quot;args&quot;: converted_args})[&quot;value&quot;]
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/webdriver.py&quot;, line 347, in execute
    self.error_handler.check_response(response)
  File &quot;/home/rose/.local/lib/python3.10/site-packages/selenium/webdriver/remote/errorhandler.py&quot;, line 229, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
  (Session info: MicrosoftEdge=123.0.2420.81); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
</pre>"""