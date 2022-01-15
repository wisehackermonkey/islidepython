from unittest import result
from ipykernel.kernelbase import Kernel
import re
class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot"
    slide_state = 0
    slides = [
    """
    Here's my confrance talk slides number 1!
    """,
    """
    Here's my confrance talk slides number 2!
    """,
    
    """
    Here's my confrance talk slides number 3!
    """,
    
    """
    Here's my confrance talk slides number 3!
    """,
    ]
    def process_slide(self,code):
        if re.search(r"^([nN]ext|>)",code):  
            return self.next_slide(code)
        if re.search(r"^([bB]ack|<)"):
            return self.prev_slide(code)
        return "sorry please enter 'next'"
    def show_slide(self,slides,slide_state):
        if len(slides) <=   slide_state + 1:
            return None
        
        next_slide = slides[slide_state]
        slide_state += 1
        return (next_slide, slide_state)
    
    def prev_slide(self):
        slide_text,slides_state = self.show_slide(self.slides,  self.slide_state - 1)
        self.slides_state = slides_state
        return slide_text
    
    def next_slide(self):   
        slide_text,slides_state = self.show_slide(self.slides, self.slide_state + 1)
        self.slides_state = slides_state
        return slide_text
        
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            
            stream_content = {'name': 'stdout', 'text': self.process_slide(code)}
            # stream_content = {'name': 'stdout', 'text': str(eval(code)) +"response from custom kernal!"}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EchoKernel)