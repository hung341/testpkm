(function($) {
    var postMessage = function(sender, data) {
        $('iframe').each(function() {
            if (this.contentWindow.postMessage) {
                this.contentWindow.postMessage({sender: sender, data: data}, "*");
            }
        });
    };
    $(window).off('message.xd_storageGet').on("message.xd_storageGet", function(e) {
        
        if (typeof e.originalEvent.data === 'object' && 'xd_storageGet' === e.originalEvent.data.sender) {
            var value = window.localStorage.getItem(e.originalEvent.data.data);
            if (value) {
                postMessage(e.originalEvent.data.receiver, value);
            }
        }
    });
    $(window).off('message.xd_storageSet').on("message.xd_storageSet", function(e) {
        if (typeof e.originalEvent.data === 'object' && 'xd_storageSet' === e.originalEvent.data.sender) {
            window.localStorage.setItem(e.originalEvent.data.data.key, e.originalEvent.data.data.value);
        }
    });
    $(window).off('message.xd_storageRemove').on("message.xd_storageRemove", function(e) {
        if (typeof e.originalEvent.data === 'object' && 'xd_storageRemove' === e.originalEvent.data.sender) {
            window.localStorage.removeItem(e.originalEvent.data.data);
        }
    });
    $(window).off('message.xd_window').on("message.xd_window", function(e) {
        if (typeof e.originalEvent.data === 'object' && 'xd_window' === e.originalEvent.data.sender) {
            window.location.href=e.originalEvent.data.data.value;
        }
    });
    $(window).off('message.xd_extGet').on("message.xd_extGet", function(e) {
        if (typeof e.originalEvent.data === 'object' && 'xd_extGet' === e.originalEvent.data.sender) {
            postMessage(e.originalEvent.data.receiver, window[e.originalEvent.data.data]);
        }
    });
}(jQuery));
