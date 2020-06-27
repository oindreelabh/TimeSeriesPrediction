var reader = new XMLHttpRequest();
	    var checkFor = "predict.html"; //Add the first link
	    var second = "alter.html"; //Add the alternative

	    reader.open('get', checkFor, true);
	    reader.onreadystatechange = checkReadyState;

	    function checkReadyState() {
	        if (reader.readyState === 4) {
	            if ((reader.status == 200) || (reader.status == 0)) {
	            document.getElementById('site').src =  checkFor;
	            }
	            else {
	           document.getElementById('site').src = second;
	            return;
	            }
	        }
	    }
	    reader.send(null);
	    