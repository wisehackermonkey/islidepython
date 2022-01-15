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
    _ ="python, really? this is valid? just wow... "
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
    Here's my confrance talk slides number 4!
    """,
    ]
    def process_slide(self,code):
        if re.search(r"^([nN]ext|>&)",code):  # next slide
            self.set_state(self.slide_state + 1)
            slide_text = self.show_slide(self.slides, self.slide_state)
            if not slide_text:
                return "end of slides"

            return slide_text
        if re.search(r"^[>]+",code): # multiple slides move forward
            num_slides_move = code.count(">")
            if not self.set_state(self.slide_state + num_slides_move):
                return f"[Slide #{self.slide_state}] invalid number of moves forward, try somthing in the range of > to {'>'*len(self.slides)}"
            return  self.show_slide(self.slides, self.slide_state)
        if re.search(r"^[<]+",code): # multiple slides move backward
            num_slides_move = code.count("<")
            if not self.set_state(self.slide_state + num_slides_move):
                return f"[Slide #{self.slide_state}] invalid number of moves backward, try somthing in the range of < to {'<'*len(self.slides)}"
            return  self.show_slide(self.slides, self.slide_state)
        if re.search(r"^[0-9]+",code):
            self.set_state(int(code.strip()) - 1 )# beause we are using arrays, and c is zero based ARG!, imbrase lisp 1 indexed people!
            slide_text = self.show_slide(self.slides, self.slide_state)
            if not slide_text:
                return f"[Slide #{self.slide_state}] invalid slide number, try somthing in the range of 0 to {len(self.slides)}"

            return slide_text
        if re.search(r"^([bB]ack|<&)",code):
            self.set_state(self.slide_state + 1)
            slide_text = self.show_slide(self.slides, self.slide_state)
            if not slide_text:
                return self.show_slide(self.slides, 0)# zero is the first slide
            return slide_text
        if re.search(r"(start|_)",code):
            return self.show_slide(self.slides, self.slide_state)
        return "sorry please enter 'next' or '>', 'back' or '<' or 'start' or _ to start the presentation"
    
    # def prev_slide(self):
    #     slide_text,slides_state = self.show_slide(self.slides,  self.slide_state - 1)
    #     self.slides_state = slides_state
    #     return slide_text
    
    # def next_slide(self):   
    #     slide_text =  self.show_slide(self.slides, self.slide_state)
    #     if not slide_text:
    #         return "End of slides"
    #     return slide_text
    def set_state(self,state):
        prev_state = self.slide_state
        self.slide_state = state
        if  0 >  self.slide_state:
            self.slide_state = 0
            return False
        elif len(self.slides) <= self.slide_state:
            self.slide_state = prev_state
            return False
        return True
    def show_slide(self,slides,slide_state):
        if len(slides) <=   slide_state or  0 > slide_state:
            return None
        next_slide = slides[slide_state]
        return next_slide    
        
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