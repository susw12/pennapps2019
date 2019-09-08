function investSelection() {
    var element = document.getElementById("invest");
    element.classList.add("selected");
    element = document.getElementById("comp");
    element.classList.remove("selected");
    var str = "compInput";
    for(var i = 1; i < 5; i++) {
        let temp = str + i;
        element = document.getElementById(temp);
        element.classList.add("d-none");
    }
    // element = document.getElementById(investInput1);
    // element.classList.remove("d-none");
}

function compSelection() {
    var element = document.getElementById("comp")
    element.classList.add("selected"); 
    element = document.getElementById("invest");
    element.classList.remove("selected");
    var str = "compInput";
    for(var i = 1; i < 5; i++) {
        let temp = str + i;
        element = document.getElementById(temp);
        element.classList.remove("d-none");
    }
//     element = document.getElementById(investInput1);
//     element.classList.add("d-none");
}

// #define $ jQuery
document.getElementById("god").onclick = function() {
    $.ajax({
        method: 'POST',
        url: '/register_business',
        data: {
            'uname': document.getElementById("uname").value,
            'pword': document.getElementById("pword").value,
            'bname': document.getElementById("bname").value,
            'bdesc': document.getElementById("bdesc").value,
            'image': document.getElementById("image").value,
            'location': document.getElementById("location").value,
			'email': document.getElementById("email").value,
			'website': document.getElementById("website").value
        },
        success: thisValueWillBeNullBecauseThereIsNoDataReturnedFromTheServerInThisAJAXRequest => {
            window.location.href = 'https://google.com';
        }
    });
}

static = []
static.push('<div class="container"><div class="row"><div class="col-xs-12 col-sm-6 col-md-6"><div class="well well-sm"><div class="row"><div class="col-sm-6 col-md-4"><img src="http://placehold.it/380x500" alt="" class="img-rounded img-responsive" /></div><div class="col-sm-6 col-md-8"><h4>')
// name
static.push('</h4><small><cite>')
//location
static.push('<i class="glyphicon glyphicon-map-marker"></i></cite></small><p><i class="glyphicon glyphicon-envelope"></i>')
//email
static.push('<br /><i class="glyphicon glyphicon-globe"></i><a href="');
//website
static.push('">')
//website (again)
static.push('</a></div></div></div></div></div></div>')

function buildHTML(name, loc, email, website) {
    str = static[0] + name + static[1] + loc + static[2] + email + 
          static[3] + website + static[4] + website + static[5];
    return str;
}