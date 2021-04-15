const fetchParameters = {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
        'Content-Type': 'application/json',
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
};

let playList = [];
let hyperDeckClipList = [];
let currentlyDisplayedTable = 'tableShowClips';

let currentTimeCodeInteger = 0;
let currentClipIndex ='';
let previousClipIndex ='';

const convertTimeCodeToInteger = (timeString, framerate) =>
{
    // converts to an arbitrary integer to be used for timecode comparisons
    const timeArray = timeString.split(":");
    return parseInt(timeArray[0] + timeArray[1] + timeArray[2] + timeArray[3]);
}



const getHyperDeckStatus = async () =>
{
    const response = await fetch('/status', fetchParameters);
    const data = await response.json();
    currentTimeCodeInteger =  convertTimeCodeToInteger(data['display timecode']);
    currentClipIndex =  convertTimeCodeToInteger(data['clip id']);
    if (currentClipIndex !== previousClipIndex && currentlyDisplayedTable === 'tableShowClips')
    {
        previousClipIndex = currentClipIndex;
        getClips().then((clipList => listClipsAsTable(clipList, 'H')))
    }
    return data;
}

const displayHyperDeckStatus = async () =>
{
    const data = await getHyperDeckStatus();
    /*

     <td id="tdStatus"></td>
     <td id="tdSpeed"></td>
     <td id="tdSlotId"></td>
     <td id="tdClipId"></td>
     <td id="tdSingleClipMode"></td>
     <td id="tdCurrentTimeCode"></td>
     <td id="tdVideoFormat"></td>
     <td id="tdLoop"></td>
     */
    if (data)
    {
        document.getElementById('tdStatus').innerText = `Status: ${data.status}`;
        document.getElementById('tdSpeed').innerText = `Speed: ${data.speed}%`;
        document.getElementById('tdSlotId').innerText = `Card Slot #: ${data['slot id']}`;
        document.getElementById('tdClipId').innerText = `Current Clip: ${data['clip id']}`;
        document.getElementById('tdSingleClipMode').innerText = `Play single clip?: ${data['single clip]'] ? "Yes" : "No"}`;
        document.getElementById('tdCurrentTimeCode').innerText = `Current TimeCode: ${data['display timecode']} (${currentTimeCodeInteger})`;
        document.getElementById('tdVideoFormat').innerText = `Video format: ${data['video format']}`;
        document.getElementById('tdLoop').innerText = `Status: ${data.loop ? "Yes" : "No"}`;
    }
}



const getClips = async () =>
{
    const response = await fetch('/getclips', fetchParameters);
    return await response.json();
}


const play = async (loop) =>
{
    const response = await fetch(`/play${loop ? '/loop' : ''}`, fetchParameters);
    return await response.json();
}

const stop = async (loop) =>
{
    const response = await fetch('/stop', fetchParameters);
    return await response.json();
}

const switchClipTables = (button) =>
{
    if (currentlyDisplayedTable === 'tableShowClips')
    {
        listClipsAsTable(playList, 'P');
        currentlyDisplayedTable = 'tablePlayList';
        button.innerText = "Show Clips in HyperDeck";
    }
    else
    {
        listClipsAsTable(hyperDeckClipList, 'H');
        currentlyDisplayedTable = 'tableShowClips';
        button.innerText = "Show Play List";
    }
}

const refreshClipList  = () =>
{
    getClips()
    .then((clipList =>
    {
        hyperDeckClipList = clipList;
        listClipsAsTable(clipList, 'H')
    }));
}

const addClipToPlaylist = (clip) =>
{
    if (!playList.find(playListClip => playListClip.index === clip.index ))
    {
        playList.push(clip);
    }
    listClipsAsTable(hyperDeckClipList, 'H');
}

const removeClipFromPlaylist = (clip) =>
{
    if (playList.find(playListClip => playListClip.index === clip.index ))
    {
        let updatedPlayList = [];
        for (let thisClip of playList)
        {
            if (thisClip.index !== clip.index)
                updatedPlayList.push(thisClip);
        }
        playList = updatedPlayList;
    }
    listClipsAsTable( playList, 'P');
}



const listClipsAsTable = (clipList, clipListType) =>
{
    // clipListType can be 'H' for HyperDeck clips, or 'P' for playlist
    let table = document.getElementById('tableShowClips');
    table.innerHTML = ""; //empty the table
    let row = document.createElement('tr');

    //Set headers
    let thClipIndex = document.createElement('th');
    let thClipName = document.createElement('th');
    let thClipTimeCode = document.createElement('th');
    let thClipDuration = document.createElement('th');
    let thActions = document.createElement('th');
    thClipIndex.innerText = "No.";
    thClipName.innerText = "Name";
    thClipTimeCode.innerText = "TimeCode";
    thClipDuration.innerText = "Duration";
    thActions.innerText = "Actions";
    row.appendChild(thClipIndex);
    row.appendChild(thClipName);
    row.appendChild(thClipTimeCode);
    row.appendChild(thClipDuration);
    row.appendChild(thActions);
    table.appendChild(row);

    //Find which clip is the current clip that the playhead is on:

    //Display data
    for (let clip of clipList)
    {
        let row = document.createElement('tr');
        let tdClipIndex = document.createElement('td');
        tdClipIndex.style.textAlign = "right";
        let tdClipName = document.createElement('td');
        let tdClipTimeCode = document.createElement('td');
        let tdClipDuration = document.createElement('td');
        let tdActions = document.createElement('td');

        tdClipIndex.innerText = clip.index;
        tdClipName.innerText = clip.name;
        tdClipTimeCode.innerText = clip.timecode;
        tdClipDuration.innerText = clip.duration;


        const buttonAction = document.createElement('button');
        if (clipListType === "H" && !playList.find(playListClip => playListClip.index === clip.index ))
        {
            buttonAction.onclick = () => addClipToPlaylist(clip);
            buttonAction.innerText = "Add";
        }
        else
        {
            buttonAction.onclick = () => removeClipFromPlaylist(clip);
            buttonAction.innerText = "Remove";
        }
        tdActions.appendChild(buttonAction);

        row.appendChild(tdClipIndex);
        row.appendChild(tdClipName);
        row.appendChild(tdClipTimeCode);
        row.appendChild(tdClipDuration);
        row.appendChild(tdActions);


        if (clip.index === currentClipIndex)
        {
            row.style.background = '#ddaaaa';
        }
        table.appendChild(row);
    }
}




window.addEventListener('load', function () {
    displayHyperDeckStatus()
        .then(() => getClips())
        .then((clipList =>
        {
            hyperDeckClipList = clipList;
            listClipsAsTable(clipList, 'H')
        }));
})

setInterval(displayHyperDeckStatus, 500);
