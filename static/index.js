let indexNamespace = {};

// Main
window.onload = async function loading(){
    indexNamespace.initialization();
    indexNamespace.addElementListener();
}

indexNamespace.initialization = function initialization(){

}

indexNamespace.addElementListener = function addElementListener(){
    const btn = document.getElementById("id-button");
    btn.addEventListener("click", async () => {
        const msg = document.getElementById("id-message").value;
        const img = document.getElementById("id-image").value;
        let url = "/api/addMessage?image=" + img + "&content=" + msg;
        console.log(img);
        console.log(msg);
        console.log(url);
        let response = await fetch(url);
        let json = await response.json();
        if("ok" in json){
            location.reload();
        }
    });
}


