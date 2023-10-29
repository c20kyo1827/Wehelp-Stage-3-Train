let indexNamespace = {};

// Main
window.onload = async function loading(){
    indexNamespace.initialization();
    indexNamespace.addElementListener();
}

indexNamespace.initialization = async function initialization(){
    const board = document.getElementById("id-board");
    let response = await fetch("api/getMessage");
    let json = await response.json();
    console.log(json);
    const zipArrays = [];
    const length = Math.min(json.data.message.length, json.data.image.length);
    for (let i = 0; i < length; i++) {
        zipArrays.push([json.data.message[i], json.data.image[i]]);
    }
    const cloudFront = "https://d188mmb7xma67m.cloudfront.net/";
    for(const[data, file] of zipArrays){
        console.log(data);
        console.log(file);
        // const content = document.createElement("div");
        // content.innerText = data[1];
        // const image = document.createElement("img");
        // image.classList.add("images");
        // image.src = data[2];
        // const hr = document.createElement("hr");
        // board.appendChild(content);
        // board.appendChild(image);
        // board.appendChild(hr);
    }
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


