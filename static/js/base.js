// setup csrf_token for most libraries

const __csrf_token = document.getElementsByName("csrf_token")[0].value
const __oldFetch = window.fetch

if (window.$) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", __csrf_token);
            }
        }
    });
}

if (window.axios) {
    axios.defaults.headers.common["X-CSRFToken"] = __csrf_token;
}

function __updateOptions(options) {
    const update = {...options};
    update.headers = {
        ...update.headers,
        "X-CSRFToken": __csrf_token,
    };
    return update;
}

// fetch

function __interceptFetch(url, options) {
    return __oldFetch(url, __updateOptions(options));
}

window.fetch = __interceptFetch;
