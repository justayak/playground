// soft-link this to ~/.jupyter/custom/custom.js
$(function() {
    
    setTimeout(function() {
        // we assume everything is loaded now..
        
        var has_js_click_handler = false;
        $('.CodeMirror-line').each(function(e) {
            
            if (!has_js_click_handler) {
                var code = $(this).html();
                if (code.indexOf('js_click_handler') !== -1) {
                    has_js_click_handler = true;
                     
                    console.info('found hook for {js_click_handler}: activate click handler!');

                    var lookup = null;

                    $(document).on('click', function(e) {
                        if (lookup !== null) {
                            var X = e.clientX;
                            var Y = e.clientY;

                            var kernel = IPython.notebook.kernel;

                            for (var i = 0; i < lookup.length; i++) {

                                var elem = lookup[i]
                                var painter = elem['painter'];

                                if (painter && painter.length > 0) {
                                    var x = painter[0].x;
                                    var y = painter[0].y;
                                    var w = painter[0].clientWidth;
                                    var h = painter[0].clientHeight;

                                    if (X >= x && X <= x + w &&
                                        Y >= y && Y <= y + h) {

                                        $('.CodeMirror', elem['code']).focus();

                                        var difx = X - x;
                                        var dify = Y - y;
                                        var x_hat = difx / w;
                                        var y_hat = dify / h;
                                        console.log(x_hat + ":" + y_hat);

                                        var code = "try:\n" +
                                            "    js_click_handler(" +
                                                     x_hat + "," + y_hat + "," + i +
                                            ")\n" + 
                                            "except:\n" +
                                            "    pass";

                                        kernel.execute(code);   
                                    }

                                }
                            }
                        }
                    });


                    setInterval(function() {

                        lookup = new Array($('.code_cell').length);

                        $('.code_cell').each(function(code_cell_idx) {
                            elem = {};
                            elem['code'] = $(this);
                            lookup[code_cell_idx] = elem;
                        });

                        for (i = 0; i < lookup.length; i++) {

                            elem = lookup[i];
                            painter = elem['painter']
                            if (typeof painter === 'undefined') {
                                painter = $('.output_subarea', elem['code']);
                                if (painter.length > 0) {
                                    elem['painter'] = $('img', painter);
                                }
                            }

                        }


                    }, 500);
                
                
                }
            }
            
        });
        
        
    }, 1000);
    
});