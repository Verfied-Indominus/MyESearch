let researcher_form = document.getElementById("researcher_signup");

// researcher_form.addEventListener("onsubmit", function(event){
//     alert('This not working?');
//     event.preventDefault();
//     researcher_form.innerHTML = `<h1>TEST</h1>`;
//     return false;
// });


async function trial(){
    let x = 0;
    let researcher_form = document.getElementById("researcher_signup");
    let selected = document.getElementsByClassName('selected');
    let selected_items = [];
    for (let i of selected){
        selected_items[x] = i.innerHTML;
        x += 1;
    };
    alert(selected_items);
    selected = await getResearchInterests(selected_items);
    researcher_form.preventDefault;
};



async function getResearchInterests(selected){
    return await fetch(`/interests/${JSON.stringify({'selected': selected})}`);
};