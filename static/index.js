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
        const imgFile = document.getElementById("id-image").files[0];
        if(msg == "" || imgFile == ""){
            console.log("Empty");
            return;
        }
        let url = "/api/addMessage";
        const formData = new FormData();
        formData.append("image", imgFile);
        formData.append("content", msg);
        let response = await fetch(url,
                {
                    method: "POST",
                    body: formData,
                    headers: {
                        "Content-Type": "application/json; charset=UTF-8"
                    }
                }
            );
        let json = await response.json();
        if("ok" in json){
            location.reload();
        }
    });
}


