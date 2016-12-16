def show_cursor(context):
    code = '''
        var prevDot;
        document.onmousemove = handleMouseMove;

        function   handleMouseMove(event) {
            var dot, eventDoc, doc, body, pageX, pageY;

            event = event || window.event;
            if (event.pageX == null && event.clientX != null)    {
                eventDoc = event.target && event.target.ownerDocument || document;
                doc = eventDoc.documentElement;
                body = eventDoc.body;

                event.pageX = event.clientX +
                          (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
                          (doc && doc.clientLeft || body && body.clientLeft || 0);
                event.pageY = event.clientY +
                          (doc && doc.scrollTop || body && body.scrollTop || 0) -
                          (doc && doc.clientTop || body && body.clientTop || 0);
            }
            dot = document.createElement('div');
            dot.style.backgroundColor = "black";
            dot.style.position = "absolute";
            dot.style.height = "15px"
            dot.style.width = "15px"
            dot.style.left = event.pageX + "px";
            dot.style.top = event.pageY + "px";

            if (prevDot) {
                document.body.removeChild(prevDot);
            }

            document.body.appendChild(dot);
            prevDot = dot;
        }
        '''
    context.browser.execute_script(code)


