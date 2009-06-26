# -*- coding: utf-8 -*-
# Copyright (c) 2009 by Leandro Lucarella, Roberto Alsina
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

try:
    import aafigure
    import aafigure.pdf
    HAS_AAFIG=True
except ImportError:
    HAS_AAFIG=False
    
from docutils import nodes
from docutils.nodes import General, Inline, Element, literal_block
from docutils.parsers.rst import directives
from docutils.parsers.rst import nodes
from reportlab.graphics import renderPDF
from docutils.parsers import rst

class Aanode(General, Inline, Element):
    children = ()

    def __init__(self, flowable, rawsource='', *children, **attributes):
        self.rawsource = rawsource
        self.flowable=flowable
        Element.__init__(self, rawsource, *children, **attributes)
    

class Aafig(rst.Directive):
    """
    Directive to insert an ASCII art figure to be rendered by aafigure.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = dict(
        scale        = float,
        line_width   = float,
        background   = str,
        foreground   = str,
        fill         = str,
        aspect       = float,
        textual      = directives.flag,
        proportional = directives.flag,
    )

    def run(self):

        if 'textual' in self.options:
            self.options['textual'] = True
        if 'proportional' in self.options:
            self.options['proportional'] = True
        try:
            if HAS_AAFIG:
                visitor = aafigure.process(
                    '\n'.join(self.content),
                    aafigure.pdf.PDFOutputVisitor,
                    options=self.options
                )
                return [Aanode(renderPDF.GraphicsFlowable(visitor.drawing))]
        except:
            pass
        return [literal_block(text='\n'.join(self.content))]
        
directives.register_directive('aafig', Aafig)
directives.register_directive('aafigure', Aafig)