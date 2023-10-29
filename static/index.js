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
        const msg = document.getElementById("id-message");
        const img = document.getElementById("id-image");
        if(msg == "" || img == undefined){
            console.log("Empty");
            return;
        }
        let url = "/api/addMessage";
        const formData = new FormData(document.getElementById("id-form"));
        console.log(formData);
        let response = await fetch(url,
                {
                    method: "POST",
                    body: formData
                }
            );
        let json = await response.json();
        if("ok" in json){
            location.reload();
        }
    });
}


