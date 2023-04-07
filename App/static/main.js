let ol = document.getElementById('overlay');
let messages;
let run = false;

function pageLoad(){
    endLoad();
}

function getMessages(msg){
    if (msg.length > 0){
        UIkit.notification({
            message: msg,
            status: 'primary',
            pos: 'top-center',
            timeout: 7000
        });
    }
}

window.addEventListener('load', async function (){
    pageLoad();
    await update();
});

let departments = {
    'Engineering': [
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research',
    ],
    'Food &amp; Agriculture': [
        'Agricultural Economics and Extension',
        'Food Production',
        'Publications and Communications Unit',
        'University Farms',
        'Geography'
    ],
    'Humanities &amp; Education': [
        'School of Education',
        'Centre for Language Learning',
        'Creative and Festival Arts',
        'History',
        'Literary, Cultural and Communication Studies',
        'Modern Languages and Linguistics',
        'The Archaeology Centre',
        'The Centre for Language Learning',
        "The Family Development and Children's Research Centre (FDCRC)",
        'The Film Programme'
    ],
    'Law': [
        'Faculty of Law'
    ],
    'Medical Sciences': [
        'Schools of Medicine',
        'Schools of Optometry',
        'Schools of Dentistry',
        'Schools of Nursing',
        'Schools of Pharmacy',
        'Schools of Veterinary Medicine', 
        'Caribbean Centre for Health Systems Research and Development',
        'Centre for Medical Sciences Education',
    ],
    'Science &amp; Technology': [
        'Chemistry',
        'Physics',
        'Life Sciences',
        'Mathematics & Statistics',
        'Computing & Information Technology',
        'Cocoa Research Centre',
        'Seismic Research Unit',
        'The National Herbarium'
    ],
    'Social Sciences': [
        'Behavioural Sciences',
        'Economics',
        'Management Studies',
        'Political Science',
        'Arthur Lok Jack Graduate School for Business',
        'Caribbean Centre for Money and Finance',
        'Centre for Criminology and Criminal Justice',
        'Institute for Gender and Development Studies',
        'Institute of International Relations',
        'Entrepreneurship Unit',
        'Health Economics Unit',
        'Sir Arthur Lewis Institute of Social & Economic Studies',
        'Sustainable Economic Development Unit',
        'Business Development Unit',
    ],
    'Sport': [
        'St. Augustine Academy of Sport'
    ],
}

let departments2 = {
    'Engineering': [
        'Chemical Engineering',
        'Civil & Environmental Engineering',
        'Mechanical & Manufacturing Engineering',
        'Geomatics Engineering & Land Management',
        'Engineering Institute',
        'Electrical & Computer Engineering',
        'Mechanical and Manufacturing Enterprise Research',
    ],
    'Food & Agriculture': [
        'Agricultural Economics and Extension',
        'Food Production',
        'Publications and Communications Unit',
        'University Farms',
        'Geography'
    ],
    'Humanities & Education': [
        'School of Education',
        'Centre for Language Learning',
        'Creative and Festival Arts',
        'History',
        'Literary, Cultural and Communication Studies',
        'Modern Languages and Linguistics',
        'The Archaeology Centre',
        'The Centre for Language Learning',
        "The Family Development and Children's Research Centre (FDCRC)",
        'The Film Programme'
    ],
    'Law': [
        'Faculty of Law'
    ],
    'Medical Sciences': [
        'Schools of Medicine',
        'Schools of Optometry',
        'Schools of Dentistry',
        'Schools of Nursing',
        'Schools of Pharmacy',
        'Schools of Veterinary Medicine', 
        'Caribbean Centre for Health Systems Research and Development',
        'Centre for Medical Sciences Education',
    ],
    'Science & Technology': [
        'Chemistry',
        'Physics',
        'Life Sciences',
        'Mathematics & Statistics',
        'Computing & Information Technology',
        'Cocoa Research Centre',
        'Seismic Research Unit',
        'The National Herbarium'
    ],
    'Social Sciences': [
        'Behavioural Sciences',
        'Economics',
        'Management Studies',
        'Political Science',
        'Arthur Lok Jack Graduate School for Business',
        'Caribbean Centre for Money and Finance',
        'Centre for Criminology and Criminal Justice',
        'Institute for Gender and Development Studies',
        'Institute of International Relations',
        'Entrepreneurship Unit',
        'Health Economics Unit',
        'Sir Arthur Lewis Institute of Social & Economic Studies',
        'Sustainable Economic Development Unit',
        'Business Development Unit',
    ],
    'Sport': [
        'St. Augustine Academy of Sport'
    ],
}

let dpt_section = document.getElementById("department_section");
let dpt_listing = document.getElementById("department_listing");

function get_selection(btn){
    let dpt_section = document.getElementById("department_section");
    let dpt_listing = document.getElementById("department_listing");
    fac = btn.childNodes[0].innerHTML.trim();
    if (fac === "All"){
        dpt_section.style.display = 'none';
    }
    else{
        dpt_section.style.display = 'block';
        let html = '';
        for (let dpt in departments[fac]){
            html += `
                <li data-faculty="${fac}" uk-filter-control="filter: [data-department='${departments[fac][dpt]}']; group: data-department"><a href=""> ${departments[fac][dpt]} </a></li>
            `;
        }
        dpt_listing.innerHTML = html;
    }
}

window.addEventListener("DOMContentLoaded", () => {
    let re_faculty = document.getElementById("re_faculty_select");
    let re_department = document.getElementById("re_department_select");

    let stu_faculty = document.getElementById("stu_faculty_select");
    let stu_department = document.getElementById("stu_department_select");

    let pro_faculty = document.getElementById("profile_faculty_select");
    let pro_department = document.getElementById("profile_department_select");

    let int_sel = document.getElementById('interests_select');
    let int_tarea = document.getElementById('interests_textarea');
    let int_tarea_hidden = document.getElementById('interests_textarea_hidden');

    try {
        re_faculty.onchange = function() {
            let html = '';
        
            for (let index in departments2[re_faculty.value]){
                html += `
                    <option value="${departments2[re_faculty.value][index]}">${departments2[re_faculty.value][index]}</option>
                `;
            }
        
            re_department.innerHTML = html;
        }
    } catch (error) {
        console.log(error);
    }

    try {
        stu_faculty.onchange = function() {
            let html = '';
        
            for (let index in departments2[stu_faculty.value]){
                html += `
                    <option value="${departments2[stu_faculty.value][index]}">${departments2[stu_faculty.value][index]}</option>
                `;
            }
        
            stu_department.innerHTML = html;
        }
    } catch (error) {
        console.log(error);
    }

    try {
        pro_faculty.onchange = function() {
            let html = '';
        
            for (let index in departments2[pro_faculty.value]){
                html += `
                    <option value="${departments2[pro_faculty.value][index]}">${departments2[pro_faculty.value][index]}</option>
                `;
            }
        
            pro_department.innerHTML = html;
        }
    } catch (error) {
        console.log(error);
    }

    try{
        int_sel.onchange = function() {
            let text = int_tarea.value;
            let interest = int_sel.value;
            if (!(text.includes(interest+"\n")) && !(text.includes(interest)) && text != ""){
                int_tarea.value = text + "\n" + interest;
            }
            else {
                int_tarea.value = interest;
            }
            int_tarea_hidden.value = int_tarea.value;
        }
    } catch (error){
        console.log(error);
    }

    let re_bar = document.getElementById('js-researcher-progressbar');
    let stu_bar = document.getElementById('js-student-progressbar');
    let pro_bar = document.getElementById('js-profile-progressbar');
    let pub_bar = document.getElementById('js-publication-progressbar');
    let pro_pub_bar = document.getElementById('js-pro-publication-progressbar');

    let re_img = document.getElementById('researcher-img-name');
    let stu_img = document.getElementById('student-img-name');
    let pro_img = document.getElementById('profile-img-name');
    let pub_name = document.getElementById('publication-name');
    let pro_pub_name = document.getElementById('pro-publication-name');

    UIkit.upload('#researcher-upload', {

        url: '/filename',
        multiple: false,
    
        beforeSend: function () {
            console.log('beforeSend', arguments);
        },
        beforeAll: function () {
            console.log('beforeAll', arguments);
        },
        load: function () {
            console.log('load', arguments);
        },
        error: function () {
            console.log('error', arguments);
        },
        complete: function () {
            console.log('complete', arguments);
        },
    
        loadStart: function (e) {
            console.log('loadStart', arguments);
    
            re_bar.removeAttribute('hidden');
            re_bar.max = e.total;
            re_bar.value = e.loaded;
        },
    
        progress: function (e) {
            console.log('progress', arguments);
    
            re_bar.max = e.total;
            re_bar.value = e.loaded;
        },
    
        loadEnd: function (e) {
            console.log('loadEnd', arguments);
    
            re_bar.max = e.total;
            re_bar.value = e.loaded;
        },
    
        completeAll: function () {
            console.log('completeAll', arguments);
    
            setTimeout(function () {
                re_bar.setAttribute('hidden', 'hidden');
            }, 1000);
    
            re_img.innerHTML = `Image Uploaded: ${arguments[0].responseText}`;
        }
    
    });
    
    UIkit.upload('#student-upload', {
    
        url: '/filename',
        multiple: false,
    
        beforeSend: function () {
            console.log('beforeSend', arguments);
        },
        beforeAll: function () {
            console.log('beforeAll', arguments);
        },
        load: function () {
            console.log('load', arguments);
        },
        error: function () {
            console.log('error', arguments);
        },
        complete: function () {
            console.log('complete', arguments);
        },
    
        loadStart: function (e) {
            console.log('loadStart', arguments);
    
            stu_bar.removeAttribute('hidden');
            stu_bar.max = e.total;
            stu_bar.value = e.loaded;
        },
    
        progress: function (e) {
            console.log('progress', arguments);
    
            stu_bar.max = e.total;
            stu_bar.value = e.loaded;
        },
    
        loadEnd: function (e) {
            console.log('loadEnd', arguments);
    
            stu_bar.max = e.total;
            stu_bar.value = e.loaded;
        },
    
        completeAll: function () {
            console.log('completeAll', arguments);
    
            setTimeout(function () {
                stu_bar.setAttribute('hidden', 'hidden');
            }, 1000);
    
            stu_img.innerHTML = `Image Uploaded: ${arguments[0].responseText}`;
        }
    
    });
    
    UIkit.upload('#profile-upload', {
    
        url: '/filename',
        multiple: false,
    
        beforeSend: function () {
            console.log('beforeSend', arguments);
        },
        beforeAll: function () {
            console.log('beforeAll', arguments);
        },
        load: function () {
            console.log('load', arguments);
        },
        error: function () {
            console.log('error', arguments);
        },
        complete: function () {
            console.log('complete', arguments);
        },
    
        loadStart: function (e) {
            console.log('loadStart', arguments);
    
            pro_bar.removeAttribute('hidden');
            pro_bar.max = e.total;
            pro_bar.value = e.loaded;
        },
    
        progress: function (e) {
            console.log('progress', arguments);
    
            pro_bar.max = e.total;
            pro_bar.value = e.loaded;
        },
    
        loadEnd: function (e) {
            console.log('loadEnd', arguments);
    
            pro_bar.max = e.total;
            pro_bar.value = e.loaded;
        },
    
        completeAll: function () {
            console.log('completeAll', arguments);
    
            setTimeout(function () {
                pro_bar.setAttribute('hidden', 'hidden');
            }, 1000);
    
            pro_img.innerHTML = `Image Uploaded: ${arguments[0].responseText}`;
        }
    
    });
    
    UIkit.upload('#publication-upload', {
    
        url: '/filename',
        multiple: false,
    
        beforeSend: function () {
            console.log('beforeSend', arguments);
        },
        beforeAll: function () {
            console.log('beforeAll', arguments);
        },
        load: function () {
            console.log('load', arguments);
        },
        error: function () {
            console.log('error', arguments);
        },
        complete: function () {
            console.log('complete', arguments);
        },
    
        loadStart: function (e) {
            console.log('loadStart', arguments);
    
            pub_bar.removeAttribute('hidden');
            pub_bar.max = e.total;
            pub_bar.value = e.loaded;
        },
    
        progress: function (e) {
            console.log('progress', arguments);
    
            pub_bar.max = e.total;
            pub_bar.value = e.loaded;
        },
    
        loadEnd: function (e) {
            console.log('loadEnd', arguments);
    
            pub_bar.max = e.total;
            pub_bar.value = e.loaded;
        },
    
        completeAll: function () {
            console.log('completeAll', arguments);
    
            setTimeout(function () {
                pub_bar.setAttribute('hidden', 'hidden');
            }, 1000);
    
            pub_name.innerHTML = `File Uploaded: ${arguments[0].responseText}`;
        }
    
    });

    UIkit.upload("#pro-publication-upload", {

    url: '/filename',
    multiple: false,

    beforeSend: function () {
    console.log('beforeSend', arguments);
    },
    beforeAll: function () {
    console.log('beforeAll', arguments);
    },
    load: function () {
    console.log('load', arguments);
    },
    error: function () {
    console.log('error', arguments);
    },
    complete: function () {
    console.log('complete', arguments);
    },

    loadStart: function (e) {
    console.log('loadStart', arguments);

    pro_pub_bar.removeAttribute('hidden');
    pro_pub_bar.max = e.total;
    pro_pub_bar.value = e.loaded;
    },

    progress: function (e) {
    console.log('progress', arguments);

    pro_pub_bar.max = e.total;
    pro_pub_bar.value = e.loaded;
    },

    loadEnd: function (e) {
    console.log('loadEnd', arguments);

    pro_pub_bar.max = e.total;
    pro_pub_bar.value = e.loaded;
    },

    completeAll: function () {
    console.log('completeAll', arguments);

    setTimeout(function () {
    pro_pub_bar.setAttribute('hidden', 'hidden');
    }, 1000);

    pro_pub_name.innerHTML = `File Uploaded: ${arguments[0].responseText}`;
    }

    });

});

function removeLast(){
    let int_tarea = document.getElementById('interests_textarea');
    let int_tarea_hidden = document.getElementById('interests_textarea_hidden');

    let arr = int_tarea.value.split(/\r?\n/);
    arr.pop();
    if (arr.length > 0){
        text = arr.join("\n");
    }
    else {
        text = "";
    }
    int_tarea.value = text;
    int_tarea_hidden.value = text;
}

async function getInterests(){
    let x = 0;
    let researcher_form = document.getElementById("researcher_signup");
    let selected = document.getElementsByClassName('selected');
    let selected_items = [];
    for (let i of selected){
        selected_items[x] = i.innerHTML;
        x += 1;
    };
    selected = await addResearchInterests(selected_items);
    researcher_form.preventDefault;
}

async function addResearchInterests(selected){
    return await fetch(`/interests/${JSON.stringify({'selected': selected})}`);
}


async function reSubscribe(btn, user_id, re_id, name){
    let response = await fetch(`/subscribe/researcher/${user_id}/${re_id}`);
    let text = await response.json();
    let state = "";
    if (text['text'].includes('check')){
        state = "subscribed to";
    }
    else {
        state = "unsubscribed from";
    }
    UIkit.notification({
        message: `You have ${state} ${name}`,
        status: 'primary',
        pos: 'top-center',
        timeout: 7000
    });
    btn.parentNode.innerHTML = text['text'];
}

async function topSubscribe(btn, user_id, top_id, name){
    let response = await fetch(`/subscribe/topic/${user_id}/${top_id}`);
    let text = await response.json();
    let state = "";
    if (text['text'].includes('check')){
        state = "subscribed to";
    }
    else {
        state = "unsubscribed from";
    }
    UIkit.notification({
        message: `You have ${state} ${name}`,
        status: 'primary',
        pos: 'top-center',
        timeout: 7000
    });
    btn.parentNode.innerHTML = text['text'];
}



// let follow = document.getElementById('follow-pub'); //follow button in publication page
// let follow_sub = document.getElementById('follow-sub'); // follow button in researcher profile page

// let unfollowhtml = `Follow<span class="uk-margin-small-left" uk-icon="plus-circle"></span>`;
// let followhtml = `Following<span class="uk-margin-small-left" uk-icon="check"></span>`;
// if (response){
//     follow.innerHTML = followhtml;
// } else {
//     follow.innerHTML = unfollowhtml;
// }

async function addToLibrary(btn, user_id, pub_id){
    let response = await fetch(`/addtolibrary/${user_id}/${pub_id}`);
    let text = await response.json();
    let state = "";
    if (text['text'].includes('In')){
        state = "added to";
    }
    else {
        state = "removed from";
    }
    UIkit.notification({
        message: `Publication ${state} your Library`,
        status: 'primary',
        pos: 'top-center',
        timeout: 7000
    });
    btn.innerHTML = text['text'];
}

async function removeFromLibrary(user_id, pub_id){
    await fetch(`/removefromlibrary/${user_id}/${pub_id}`);
}

// functions to add to recents and library

async function addToRecents(user_id, pub_id){
    await fetch(`/addtorecents/${user_id}/${pub_id}`);
}

// function to add read to publication
async function addRead(id){
    if (pastDate() || analytics('read') || identifier(id)){
        await fetch(`/publication/addread/${id}`);
    }
}

// function to add download to publication
async function addDownload(id){
    if (pastDate() || analytics('download') || identifier(id)){
        await fetch(`/publication/adddownload/${id}`);
    }
}

// function to add citation to publication
async function addCitation(id){
    if (pastDate() || analytics('citation') || identifier(id)){
        let response = await fetch(`/publication/addcitation/${id}`);
        let citation = await response.json();
        let cite_body = document.getElementById('citation-modal-body');
        let html = `
            <h4 class="uk-modal-title">Chicago</h4>
            <div>${citation['citation'][0]}</div>
            <h4 class="uk-modal-title">APA</h4>
            <div>${citation['citation'][1]}</div>
            <h4 class="uk-modal-title">MLA</h4>
            <div>${citation['citation'][2]}</div>
        `;
        cite_body.innerHTML = html;
    }
    else {
        let response = await fetch(`/publication/getcitation/${id}`);
        let citation = await response.json();
        let cite_body = document.getElementById('citation-modal-body');
        let html = `
            <h4 class="uk-modal-title">Chicago</h4>
            <div>${citation['citation'][0]}</div>
            <h4 class="uk-modal-title">APA</h4>
            <div>${citation['citation'][1]}</div>
            <h4 class="uk-modal-title">MLA</h4>
            <div>${citation['citation'][2]}</div>
        `;
        cite_body.innerHTML = html;
    }
}

// function to add search to publication
async function addSearchPublication(id){
    if (pastDate() || analytics('publicationSearch') || identifier(id)){
        await fetch(`/publication/addsearch/${id}`);
    }
}

// function to add view for profile
async function addView(id){
    if (pastDate() || analytics('profileView') || identifier(id)){
        await fetch(`/profile/addview/${id}`);
    }
}


// function to add search for profile
async function addSearchResearcher(id){
    if (pastDate() || analytics('researcherSearch') || identifier(id)){
        await fetch(`/profile/addsearch/${id}`);
    }
}

async function test(){
    await fetch('/test');
}

// background updater for researcher publications
async function update(){
    if (sessionStorage.getItem('update') == null){
        sessionStorage.setItem('update', true);
        let response = await fetch('/update');
        console.log(response.text);
    }
}

async function update2(){
    await fetch('/update');
}

function identifier(id){
    if (localStorage.getItem('id') == null){
        localStorage.setItem('id', id);
        return true;
    }
    if (localStorage.getItem('id').includes(id)){
        return false;
    }
    else {
        localStorage.setItem('id', localStorage.getItem('id').concat(', ', id));
        return true;
    }
}

function analytics(term){
    if (localStorage.getItem('analytics') == 'null' || localStorage.getItem('analytics') == null){
        localStorage.setItem('analytics', term);
        return true;
    }
    if (localStorage.getItem('analytics').includes(term)){
        return false;
    }
    else {
        localStorage.setItem('analytics', localStorage.getItem('analytics').concat(', ', term));
        return true;
    }
}

function getDate(){
    let date = new Date();
    let day = date.getDate();
    let month = date.getMonth()+1;
    let year = date.getFullYear();
    date = `${day}/${month}/${year}`;
    return date;
}

function pastDate(){
    let date = getDate();
    if (localStorage.getItem('date') == 'null'){
        localStorage.setItem('date', date);
        localStorage.setItem('analytics', 'null');
        return true;
    }
    else if (date > localStorage.getItem('date')){
        localStorage.setItem('date', date);
        localStorage.setItem('analytics', 'null');
        return true;
    }
    else{
        return false;
    }
}


async function loadResearchers(researchers){
    let ar_ul = document.getElementById('all_researcher_ul');
    let re_num = document.getElementById('researcher_num');

    re_num.innerHTML = `All Researchers (${researchers.length} Present)`;
    let html1 = "";
    for (let x = 0; x < researchers.length; x += 1){
        window.setTimeout(() => {
            let re = researchers[x];
            html1 += `
                <li data-name="${re['first_name'][0].toUpperCase()}" data-faculty="${re['faculty']}" data-department="${re['department']}" style="padding: 0 30px; transform: translateY(0px);" class="uk-margin-medium-top">
                    <div style="cursor: pointer;" onclick="window.location='/profile/${re['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex hvr-grow-shadow uk-height-1-1">
                        <div class="uk-margin-small-top uk-margin-small-bottom uk-width-1-1 uk-text-center">
                            <div class="uk-flex uk-flex-center uk-margin-small-bottom">`;
                                let html2 = "";
                                if (re['image_url'] != null){
                                    html2 = `<div class="uk-border-circle uk-background-cover" data-src="${re['image_url']}" alt="" style="width: 200px; height: 200px;" uk-img></div>`; 
                                }
                                else{
                                    html2 = `<div class="uk-border-circle uk-background-cover" data-src="/static/images/unknown.png" alt="" style="width: 200px; height: 200px;" uk-img></div>`; 
                                }
                                html1 += html2;
                                html1 += `
                            </div>
                            <h4 class="uk-margin-auto uk-margin-small-top"> ${re['title']} ${re['first_name']} ${re['last_name']} </h4>
                            <div> ${re['position']} </div>
                            <div> ${re['faculty']} </div>
                            <div> ${re['department']} </div>
                        </div>
                    </div> 
                </li>
            `;
            console.log(re['subs']);
            if (x % (researchers.length - 1) == 0){
                ar_ul.innerHTML = html1;
            }
        }, 0);
    } 
    
    endLoad();
}

async function loadPublications(publications){
    let ap_ul = document.getElementById('all_publication_ul');
    let pub_num = document.getElementById('publication_num');
    pub_num.innerHTML = `All Publications (${publications.length} Present)`;
    let html1 = "";
    for (let x = 0; x < publications.length; x += 1){
        let pub = publications[x];
        window.setTimeout(() => {
            html1 += `
                <li data-cite="${pub['citations']}" data-year="`; if (pub['publication_date'] <= new Date().getFullYear() - 11){html1 += `${new Date().getFullYear() - 11}`;}else{html1 += `${pub['publication_date']}`;} html1 += `" data-type="${pub['pub_type']}" data-name="${pub['title'][0].toUpperCase()}" style="padding: 0 30px; transform: translateY(0px);" class="uk-margin-medium-top">
                    <div style="cursor: pointer;" onclick="window.location='/publication/${pub['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow uk-height-1-1">
                        <div style="height: 140px; width: 100px;" class="uk-background-contain" data-src="/static/images/publications/${pub['pub_type']}.png" uk-img></div>
                        <div class="uk-margin-small-left uk-width-expand">
                            <h4 class="uk-margin-remove"> ${titleCase(pub['title'])} </h4>
                            <div class="uk-text-middle uk-margin-small-bottom"><span class="uk-label uk-margin-small-right"> ${pub['pub_type']} </span>`;
                                if (pub['publication_date'] != 1){
                                    html1 += `${pub['publication_date']}`;
                                }
                                html1 += `</div>
                            <div>`;
                                let coauthors = [];
                                if (pub['authors'].length < 3){
                                    for (let re of pub['authors']){
                                        html1 += `<a href="/profile/${re['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (re['image_url'] != null){
                                                html1 += `${re['image_url']}`;
                                            } 
                                            else {
                                                html1 += '/static/images/unknown.png';
                                            }   
                                        html1 += `');" uk-icon></span> ${re['first_name']}  ${re['last_name']} </a>`;
                                    }
                                    if (pub['coauthors'] != "" && pub['coauthors'] != null){
                                        coauthors = pub['coauthors'].split(', ');
                                        let limit = 3 - pub['authors'].length;
                                        if (limit < coauthors.length){
                                            for (let n = 0; n < limit; n += 1){
                                                html1 += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                            html1 += `+${coauthors.length - limit} More`;
                                        }
                                        else {
                                            for (let n = 0; n < coauthors.length; n += 1){
                                                html1 += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                        }
                                    }
                                }
                                else{
                                    for (let n = 0; n < 3; n += 1){
                                        html1 += `<a href="/profile/${pub['authors'][n]['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (pub['authors'][n]['image_url'] != null){
                                                html1 += `${pub['authors'][n]['image_url']}`;
                                            } 
                                            else {
                                                html1 += '/static/images/unknown.png';
                                            }   
                                        html1 += `');" uk-icon></span> ${pub['authors'][n]['first_name']}  ${pub['authors'][n]['last_name']} </a>`;
                                    }
                                    if (pub['authors'].length > 3){
                                        html1 += `+${(pub['authors'].length + coauthors.length) - 3} More`;
                                    }
                                }
                            html1 += `</div>
                        </div>
                    </div>
                </li>
            `;
            if (x % (publications.length - 1) == 0){
                ap_ul.innerHTML = html1;
            }
        }, 0); 
    }
    
    endLoad();
}

function titleCase(str) {
    return str.toLowerCase().replace(/\b\w/g, s => s.toUpperCase());
}

async function loadSuggestions(data, id){
    let tabs = document.getElementById('tabs');
    let switcher = document.getElementById('switcher');
    let researchers = data[0];
    let topics = data[1];
    let popular = data[2];

    let html = "";
    if (researchers.length > 1){
        html += '<li><a href="">More from the authors</a></li>';
    }
    if (topics.length > 1){
        html += '<li><a href="">More from the topics</a></li>';
    }
    html += '<li><a href="">Most popular</a></li>';
    tabs.innerHTML = html;

    html = "";
    if (researchers.length > 1){
        html += '<li class="uk-grid uk-margin-remove uk-child-width-1-2 scroll uk-padding uk-padding-remove-horizontal uk-padding-remove-top" uk-grid uk-height-viewport="offset-bottom: 40;" uk-height-match="target: div > .uk-card">';
        for (let p of researchers){
            if (parseInt(p['id']) != parseInt(id)){
                html += `
                    <div style="padding: 0 30px">
                        <div style="cursor: pointer;" onclick="window.location='/publication/${p['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow">
                            <div style="height: 140px; width: 100px;" class="uk-background-contain" data-src="/static/images/publications/${p['pub_type']}.png" uk-img></div>
                            <div class="uk-margin-small-left uk-width-expand">
                                <h4 class="uk-margin-remove"> ${titleCase(p['title'])} </h4>
                                <div class="uk-text-middle uk-margin-small-bottom"><span class="uk-label uk-margin-small-right"> ${p['pub_type']} </span>`;
                                if (p['publication_date'] != 1){
                                    html += `${p['publication_date']}`;
                                }
                                html += ` </div>
                                <div>`;
                                    let coauthors = [];
                                    if (p['authors'].length < 2){
                                        for (let re of p['authors']){
                                            html += `<a href="/profile/${re['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                                if (re['image_url'] != null){
                                                    html += `${re['image_url']}`;
                                                } 
                                                else {
                                                    html += '/static/images/unknown.png';
                                                }   
                                            html += `');" uk-icon></span> ${re['first_name']}  ${re['last_name']} </a>`;
                                        }
                                        if (p['coauthors'] != "" && p['coauthors'] != null){
                                            coauthors = p['coauthors'].split(', ');
                                            let limit = 2 - p['authors'].length;
                                            if (limit < coauthors.length){
                                                for (let n = 0; n < limit; n += 1){
                                                    html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                                }
                                                html += `+${coauthors.length - limit} More`;
                                            }
                                            else {
                                                for (let n = 0; n < coauthors.length; n += 1){
                                                    html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                                }
                                            }
                                        }
                                    }
                                    else{
                                        for (let n = 0; n < 2; n += 1){
                                            html += `<a href="/profile/${p['authors'][n]['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                                if (p['authors'][n]['image_url'] != null){
                                                    html += `${p['authors'][n]['image_url']}`;
                                                } 
                                                else {
                                                    html += '/static/images/unknown.png';
                                                }   
                                            html += `');" uk-icon></span> ${p['authors'][n]['first_name']}  ${p['authors'][n]['last_name']} </a>`;
                                        }
                                        if (p['authors'].length > 2){
                                            html += `+${(p['authors'].length + coauthors.length) - 2} More`;
                                        }
                                    }    
                                html += `</div>
                            </div>
                        </div>
                    </div>
                `;
            }
        }
        html += '</li>';
        switcher.innerHTML += html;
    }

    html = "";
    if (topics.length > 1){
        html += '<li class="uk-grid uk-margin-remove uk-child-width-1-2 scroll uk-padding uk-padding-remove-horizontal uk-padding-remove-top" uk-grid uk-height-viewport="offset-bottom: 40;" uk-height-match="target: div > .uk-card">';
        for (let p of topics){
            if (parseInt(p['id']) != parseInt(id)){
                html += `
                    <div style="padding: 0 30px">
                        <div style="cursor: pointer;" onclick="window.location='/publication/${p['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow">
                            <div style="height: 140px; width: 100px;" class="uk-background-contain" data-src="/static/images/publications/${p['pub_type']}.png" uk-img></div>
                            <div class="uk-margin-small-left uk-width-expand">
                                <h4 class="uk-margin-remove"> ${titleCase(p['title'])} </h4>
                                <div class="uk-text-middle uk-margin-small-bottom"><span class="uk-label uk-margin-small-right"> ${p['pub_type']} </span>`;
                                if (p['publication_date'] != 1){
                                    html += `${p['publication_date']}`;
                                }
                                html += ` </div>
                                <div>`;
                                    let coauthors = [];
                                    if (p['authors'].length < 2){
                                        for (let re of p['authors']){
                                            html += `<a href="/profile/${re['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                                if (re['image_url'] != null){
                                                    html += `${re['image_url']}`;
                                                } 
                                                else {
                                                    html += '/static/images/unknown.png';
                                                }   
                                            html += `');" uk-icon></span> ${re['first_name']}  ${re['last_name']} </a>`;
                                        }
                                        if (p['coauthors'] != "" && p['coauthors'] != null){
                                            coauthors = p['coauthors'].split(', ');
                                            let limit = 2 - p['authors'].length;
                                            if (limit < coauthors.length){
                                                for (let n = 0; n < limit; n += 1){
                                                    html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                                }
                                                html += `+${coauthors.length - limit} More`;
                                            }
                                            else {
                                                for (let n = 0; n < coauthors.length; n += 1){
                                                    html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                                }
                                            }
                                        }
                                    }
                                    else{
                                        for (let n = 0; n < 2; n += 1){
                                            html += `<a href="/profile/${p['authors'][n]['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                                if (p['authors'][n]['image_url'] != null){
                                                    html += `${p['authors'][n]['image_url']}`;
                                                } 
                                                else {
                                                    html += '/static/images/unknown.png';
                                                }   
                                            html += `');" uk-icon></span> ${p['authors'][n]['first_name']}  ${p['authors'][n]['last_name']} </a>`;
                                        }
                                        if (p['authors'].length > 2){
                                            html += `+${(p['authors'].length + coauthors.length) - 2} More`;
                                        }
                                    }    
                                html += `</div>
                            </div>
                        </div>
                    </div>
                `;
            }
        }
        html += '</li>';
        switcher.innerHTML += html;
    }

    html = "";
    html += '<li class="uk-grid uk-margin-remove uk-child-width-1-2 scroll uk-padding uk-padding-remove-horizontal uk-padding-remove-top" uk-grid uk-height-viewport="offset-bottom: 40;" uk-height-match="target: div > .uk-card">';
    for (let p of popular){
        if (parseInt(p['id']) != parseInt(id)){
            html += `
                <div style="padding: 0 30px">
                    <div style="cursor: pointer;" onclick="window.location='/publication/${p['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow">
                        <div style="height: 140px; width: 100px;" class="uk-background-contain" data-src="/static/images/publications/${p['pub_type']}.png" uk-img></div>
                        <div class="uk-margin-small-left uk-width-expand">
                            <h4 class="uk-margin-remove"> ${titleCase(p['title'])} </h4>
                            <div class="uk-text-middle uk-margin-small-bottom"><span class="uk-label uk-margin-small-right"> ${p['pub_type']} </span>`;
                            if (p['publication_date'] != 1){
                                html += `${p['publication_date']}`;
                            }
                            html += ` </div>
                            <div>`;
                                let coauthors = [];
                                if (p['authors'].length < 2){
                                    for (let re of p['authors']){
                                        html += `<a href="/profile/${re['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (re['image_url'] != null){
                                                html += `${re['image_url']}`;
                                            } 
                                            else {
                                                html += '/static/images/unknown.png';
                                            }   
                                        html += `');" uk-icon></span> ${re['first_name']}  ${re['last_name']} </a>`;
                                    }
                                    if (p['coauthors'] != "" && p['coauthors'] != null){
                                        coauthors = p['coauthors'].split(', ');
                                        let limit = 2 - p['authors'].length;
                                        if (limit < coauthors.length){
                                            for (let n = 0; n < limit; n += 1){
                                                html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                            html += `+${coauthors.length - limit} More`;
                                        }
                                        else {
                                            for (let n = 0; n < coauthors.length; n += 1){
                                                html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                        }
                                    }
                                }
                                else{
                                    for (let n = 0; n < 2; n += 1){
                                        html += `<a href="/profile/${p['authors'][n]['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (p['authors'][n]['image_url'] != null){
                                                html += `${p['authors'][n]['image_url']}`;
                                            } 
                                            else {
                                                html += '/static/images/unknown.png';
                                            }   
                                        html += `');" uk-icon></span> ${p['authors'][n]['first_name']}  ${p['authors'][n]['last_name']} </a>`;
                                    }
                                    if (p['authors'].length > 2){
                                        html += `+${(p['authors'].length + coauthors.length) - 2} More`;
                                    }
                                }    
                            html += `</div>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    html += '</li>';
    switcher.innerHTML += html;

    endLoad();
}

async function loadProfilePubs(pubs){
    let propubs = document.getElementById('profile-pubs');
    let html = "";
    if (pubs.length > 0){
        for (let p of pubs){
            html += `
                <div style="padding: 0 30px">
                    <div style="cursor: pointer;" onclick="window.location='/publication/${p['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow">
                        <div style="height: 140px; width: 100px;" class="uk-background-contain" data-src="/static/images/publications/${p['pub_type']}.png" uk-img></div>
                        <div class="uk-margin-small-left uk-width-expand">
                            <h4 class="uk-margin-remove"> ${titleCase(p['title'])} </h4>
                            <div class="uk-text-middle uk-margin-small-bottom"><span class="uk-label uk-margin-small-right"> ${p['pub_type']} </span>`;
                            if (p['publication_date'] != 1){
                                html += `${p['publication_date']}`;
                            }
                            html += ` </div>
                            <div>`;
                                let coauthors = [];
                                if (p['authors'].length < 2){
                                    for (let re of p['authors']){
                                        html += `<a href="/profile/${re['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (re['image_url'] != null){
                                                html += `${re['image_url']}`;
                                            } 
                                            else {
                                                html += '/static/images/unknown.png';
                                            }   
                                        html += `');" uk-icon></span> ${re['first_name']}  ${re['last_name']} </a>`;
                                    }
                                    if (p['coauthors'] != "" && p['coauthors'] != null){
                                        coauthors = p['coauthors'].split(', ');
                                        let limit = 2 - p['authors'].length;
                                        if (limit < coauthors.length){
                                            for (let n = 0; n < limit; n += 1){
                                                html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                            html += `+${coauthors.length - limit} More`;
                                        }
                                        else {
                                            for (let n = 0; n < coauthors.length; n += 1){
                                                html += `<a href="https://scholar.google.com/scholar?as_vis=1&q=author:+%22${coauthors[n]}%22&hl=en&as_sdt=0,5" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('/static/images/unknown.png');" uk-icon></span> ${coauthors[n]} </a>`;
                                            }
                                        }
                                    }
                                }
                                else{
                                    for (let n = 0; n < 2; n += 1){
                                        html += `<a href="/profile/${p['authors'][n]['id']}" style="padding: 2px 3px; height: 45px;" class="uk-margin-small-right uk-border-pill uk-background-muted uk-inline uk-text-decoration-none uk-button uk-button-default uk-text-capitalize"><span class="uk-icon uk-icon-image uk-border-circle" style="height: 30px; width: 30px; background-image: url('`;
                                            if (p['authors'][n]['image_url'] != null){
                                                html += `${p['authors'][n]['image_url']}`;
                                            } 
                                            else {
                                                html += '/static/images/unknown.png';
                                            }   
                                        html += `');" uk-icon></span> ${p['authors'][n]['first_name']}  ${p['authors'][n]['last_name']} </a>`;
                                    }
                                    if (p['authors'].length > 2){
                                        html += `+${(p['authors'].length + coauthors.length) - 2} More`;
                                    }
                                }    
                            html += `</div>
                        </div>
                    </div>
                </div>
            `;
        }
        propubs.innerHTML += html;
    }

    endLoad();
}

function endLoad(){
    ol.style.opacity = '0';
    this.document.body.style.overflowY = 'auto';
    this.setTimeout(function(){
        ol.style.visibility = 'hidden';
        ol.style.display = 'none';
    }, 200);
}

async function verify_author(verifier_id, auth_id, name){
    UIkit.notification({
        message: `You have verified ${name}`,
        status: 'primary',
        pos: 'top-center',
        timeout: 7000
    });
    await fetch(`/verify/${verifier_id}/${auth_id}`);
} 

async function set_read(notif_rec_ids){
    console.log(notif_rec_ids);
    for (let rec_id of notif_rec_ids){
        await fetch(`/setread/${rec_id}`);
    }
}

async function accept_request(s_id, pub_id){
    await fetch(`/accept/${s_id}/${pub_id}`);
}

async function reject_request(s_id, pub_id){
    await fetch(`/reject/${s_id}/${pub_id}`);
}

async function followback(researcher_id, subscriber_id){
    await fetch(`/followback/${researcher_id}/${subscriber_id}`);
}

async function clear_notifications(user_id){
    let notifs_body = document.getElementById('all-notifs-body');
    notifs_body.innerHTML = `
        <div class="uk-margin-auto uk-text-center">
            <img class="uk-width-2-3" src="/static/images/noNotifs2.jpg" alt="No Notifications Present">
            <h4 class="uk-margin-remove-top">No Notifications Present</h4>
        </div>
    `;
    await fetch(`/clear/notifications/${user_id}`);
}