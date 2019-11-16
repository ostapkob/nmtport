    var  i = 0
    var id = setInterval('myFunct_1()', 1000);
    var counter= 0;
    function myFunct_1() {
        counter++;
        document.getElementById("count").innerHTML = counter;
        if (counter >10) clearInterval(id);
    }

