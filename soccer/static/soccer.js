function highlightUnderline(elem)
{
	elem.style.textDecoration="underline";
    elem.style.cursor="pointer";
    elem.style.color = "#0A0A32";
}

function createRequestInternal()
{
	var xmlhttp = null;
	if (window.XMLHttpRequest) {
		xmlhttp=new XMLHttpRequest();  // code for IE7+, Firefox, Chrome, Opera, Safari
	}
	else if (window.ActiveXObject) {
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");  // code for IE6, IE5
	}
	else {
		alert(xlInternal(0));
	}
	
	return xmlhttp;
}

function submitScoreInternal(text, parastr, elem)
{
	xmlhttp = createRequestInternal();

	if(xmlhttp != null)
	{
		xmlhttp.onreadystatechange=function() {
			if(xmlhttp.readyState == 4) {
				if(xmlhttp.status == 200) {
					elem.className = "valid";
				} else {
                    alert("not 200");
                }
			}
		};
		xmlhttp.open("POST", "submitScore", true);
		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 
		
		elem.className = "pending";

		data = "";
		if (elem.name == "bet") {
			data = "match_id=" + parastr + "&bet=" + text;
		} else {
			data = "match_id=" + parastr + "&result=" + text;
		}
/*		params = parastr.split('_');
		for (i = 0; i < params.length; i++) {
			keyval = params[i].split('.');
			data += keyval[0] + "=" + encodeURIComponent(keyval[1]) + "&";
		}
        data += "value=" + encodeURIComponent(text);
        */
		
		xmlhttp.send(data);
	}
}

function submitScore(elem)
{
	try {
        submitScoreInternal(elem.value, elem.id, elem);
	}
	catch(err) {
		alert("submitScoreInternal failed");
	}
}