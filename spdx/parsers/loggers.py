# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class StandardLogger(object):
    def log(self, msg):
        print(msg)


class FileLogger(object):
    def __init__(self, logfile):
        self.dest = logfile

    def log(self, msg):
        self.dest.write(msg + "\n")


class ErrorMessages:

    def __init__(self):
        self.messages = []
        self.context = []
    
    def push_context(self, context):
        """push some context information to better indentify where is the problem"""
        self.context.append(context)

    def pop_context(self):
        """pop the last context information"""
        self.context.pop()
    
    def append(self, message, *args, **kwargs):
        """add a message with standard python format
        the current context is prefixed to the message
        """
        message = message.format(*args, **kwargs)
        message = "".join([c + ": " for c in self.context if c]) + message
        self.messages.append(message)

    def __iter__(self):
        return self.messages.__iter__()

    def __bool__(self):
        return len(self.messages)>0

    def __nonzero__(self):
        return len(self.messages)>0
    
    def __eq__(self, b):
        if isinstance(b, ErrorMessages):
            return self.messages == b.messages
        return self.messages == b
