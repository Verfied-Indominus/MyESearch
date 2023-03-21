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
            status: 'danger',
            pos: 'top-center',
            timeout: 5000
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

let dpt_section = document.getElementById("department_section");
let dpt_listing = document.getElementById("department_listing");

function get_selection(btn){
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

let re_faculty = document.getElementById("re_faculty_select");
let re_department = document.getElementById("re_department_select");

let stu_faculty = document.getElementById("stu_faculty_select");
let stu_department = document.getElementById("stu_department_select");

re_faculty.onchange = function() {
    let html = '';

    for (let index in departments[re_faculty.value]){
        html += `
            <option value="${departments[re_faculty.value][index]}">${departments[re_faculty.value][index]}</option>
        `;
    }

    re_department.innerHTML = html;
}

stu_faculty.onchange = function() {
    let html = '';

    for (let index in departments[stu_faculty.value]){
        html += `
            <option value="${departments[stu_faculty.value][index]}">${departments[stu_faculty.value][index]}</option>
        `;
    }

    stu_department.innerHTML = html;
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


let re_bar = document.getElementById('js-researcher-progressbar');
let stu_bar = document.getElementById('js-student-progressbar');
let re_img = document.getElementById('researcher-img-name');
let stu_img = document.getElementById('student-img-name');

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

let follow = document.getElementById('follow-pub'); //follow button in publication page
let follow_sub = document.getElementById('follow-sub'); // follow button in researcher profile page

async function addToLibrary(user_id, pub_id){
    let response = await fetch(`/addtolibrary/${user_id}/${pub_id}`);
    let unfollowhtml = `Follow<span class="uk-margin-small-left" uk-icon="plus-circle"></span>`;
    let followhtml = `Following<span class="uk-margin-small-left" uk-icon="check"></span>`;
    if (response){
        follow.innerHTML = followhtml;
    } else {
        follow.innerHTML = unfollowhtml;
    }
}

// functions to add to recents and library

async function addToRecents(user_id, pub_id){
    return await fetch(`/addtorecents/${user_id}/${pub_id}`);
}

// function to add read to publication
async function addRead(id){
    if (pastDate()){
        let response = await fetch(`/publication/addread/${id}`);
    }
}

// function to add download to publication
async function addDownload(id){
    if (pastDate()){
        let response = await fetch(`/publication/adddownload/${id}`);
    }
}

// function to add citation to publication
async function addCitation(id){
    if (pastDate()){
        let response = await fetch(`/publication/addcitation/${id}`);
        let citation = await response.json();
        // add element to display citation
    }
}

// function to add search to publication
async function addSearchPublication(id){
    if (pastDate()){
        let response = await fetch(`/publication/addsearch/${id}`);
    }
}

// function to add view for profile             NOT WORKING!!!
// async function addView(id){
//     if (pastDate()){
//         let response = await fetch(`/profile/addview/${id}`);
//         console.log(response);
//     }
// }

// function to add search for profile
async function addSearchResearcher(id){
    if (pastDate()){
        let response = await fetch(`/profile/addsearch/${id}`);
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
    if (localStorage.getItem('date') == null){
        localStorage.setItem('date', date);
        return true;
    }
    if (date > localStorage.getItem('date')){
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
                    <div style="cursor: pointer;" onclick="window.location='/profile/${re['id']}'" class="uk-card uk-card-default uk-padding-small uk-flex uk-inline hvr-grow-shadow uk-height-1-1">
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
                            <h4 class="uk-margin-auto"> ${re['title']} ${re['first_name']} ${re['last_name']} </h4>
                            <div> ${re['position']} </div>
                            <div> ${re['faculty']} </div>
                            <div> ${re['department']} </div>
                        </div>
                    </div>
                </li>
            `;
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
                <li data-year="${pub['publication_date']}" data-type="${pub['pub_type']}" data-name="${pub['title'][0].toUpperCase()}" style="padding: 0 30px; transform: translateY(0px); display: none;" class="uk-margin-medium-top">
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