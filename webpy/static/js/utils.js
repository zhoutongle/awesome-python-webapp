function custAlert(title,message){
    var alertdialog = $('<div id="alertdialog" title="'+title+'"><p>'+message+'</p></div>').appendTo('body');
    alertdialog.dialog({
        bgiframe: true,
        autoOpen: true,
        resizable: false,
        modal: true,
        buttons: {
            '确定': function() {
                $(this).dialog('close');
            }
        },
        close: function(){
            alertdialog.remove();
       }
    });
}
function custConfirm(title,message,buttons){                                                                            
    var confdialog = $('<div id="confdialog" title="'+title+'"><p>'+message+'</p></div>').appendTo('body');             
    var defbuttons = {                                                                                                  
        Cancel: function() {                                                                                            
            $(this).dialog('close');                                                                                    
        },                                                                                                              
        'OK': function() {                                                                                        
            $(this).dialog('close');                                                                                    
        }                                                                                                               
    };                                                                                                                  
    confdialog.dialog({                                                                                                 
        bgiframe: true,                                                                                                 
        autoOpen: true,                                                                                                 
        resizable: false,                                                                                               
        modal: true,                                                                                                    
        buttons: buttons || defbuttons,                                                                                 
        close: function(){                                                                                              
            confdialog.remove();                                                                                        
        }                                                                                                               
    });                                                                                                                 
}
function custwarning(title,message,buttons){                                                                                                                                                                                
    var warningdialog = $('<div id="warningdialog" title="'+title+'"><p><span style="margin: 0pt 7px 20px 0pt; float: left;" class="ui-icon ui-icon-alert"/>' + message + '</p></div>').appendTo('body');
    var defbuttons = {                                                                                                  
        Cancel: function() {                                                                                            
            $(this).dialog('close');                                                                                    
        },                                                                                                              
        'OK': function() {                                                                                              
            $(this).dialog('close');                                                                                    
        }                                                                                                               
    };                                                                                                                  
    warningdialog.dialog({                                                                                              
        bgiframe: true,                                                                                                 
        autoOpen: true,                                                                                                 
        resizable: false,                                                                                               
        modal: true,                                                                                                    
        buttons: buttons || defbuttons,                                                                                
        close: function(){                                                                                             
            warningdialog.remove();                                                                                    
        }                                                                                                              
    });                                                                                                                
}
function custWarning(title,message,cancelcallback,comfirmcallback,options){                                                                                                                                            
    var warningdialog = $('<div id="warningdialog" title="'+title+'"><p><span style="margin: 0pt 7px 20px 0pt; float: left;" class="ui-icon ui-icon-alert"/>' + message + '</p></div>').appendTo('body');
    warningdialog.dialog({                                                                                             
        bgiframe: true,                                                                                                
        autoOpen: true,                                                                                                
        resizable: false,                                                                                              
        modal: true,                                                                                                   
        buttons: {                                                                                                     
            'cancel': function() {                                                                               
                $(this).dialog('close');                                                                               
                if(cancelcallback != undefined){                                                                       
                    cancelcallback();                                                                                  
                }                                                                                                      
            },                                                                                                         
            'OK': function() {                                                                                   
                $(this).dialog('close');                                                                               
                if(comfirmcallback != undefined){                                                                      
                    comfirmcallback();                                                                                 
                }                                                                                                      
            }                                                                                                          
        },                                                                                                             
        close: function(){                                                                                             
            warningdialog.remove();                                                                                    
        }                                                                                                              
    });                                                                                                                
}
function custLoading(message){                                                                                         
    var loaddialog = $('<div id="loaddialog" title="" style="min-height:75px;"><p class="loadword" style="text-align:center">' + message + '</p><p style="text-align:center">' + '<img src="static/image/ajax-loader.gif" /></p></div>').appendTo('body');
    loaddialog.dialog({                                                                                                
        bgiframe: true,                                                                                                
        autoOpen: true,                                                                                                
        resizable: false,                                                                                              
        modal: true,                                                                                                   
        height: 105,                                                                                                   
        width: 300,                                                                                                    
        close: function(){                                                                                             
            loaddialog.remove();                                                                                       
        }                                                                                                              
    });                                                                                                                
    //$('loaddialog .ui-dialog-titlebar').hide();
	loaddialog.siblings('div.ui-dialog-titlebar').remove();
}