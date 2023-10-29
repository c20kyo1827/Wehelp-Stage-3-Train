let indexNamespace = {};

// Main
window.onload = async function loading(){
    indexNamespace.initialization();
    indexNamespace.addElementListener();
}

indexNamespace.initialization = function initialization(){

}

indexNamespace.addElementListener = function addElementListener(){
    const form = document.getElementById("id-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const msg = document.getElementById("id-message");
        const img = document.getElementById("id-image");
        if(msg == "" || img == undefined){
            console.log("Empty");
            return;
        }
        let url = "/api/addMessage";
        let formData = new FormData(form);
        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
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


