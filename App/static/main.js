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