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
let currentPlayList = []
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
        getHyperDeckClips().then((clipList => listClipsAsTable(clipList, 'H')))
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



const getHyperDeckClips = async () =>
{
    const response = await fetch('/getclips', fetchParameters);
    return await response.json();
}


const play = async (loop) =>
{
    const response = await fetch(`/play${loop ? '/loop' : ''}`, fetchParameters);
    return await response.json();
}

const playNow = async (clipIndex, loop) =>
{
    const response = await fetch(`/playclip/${clipIndex}${loop ? '/loop' : ''}`, fetchParameters);
    return await response.json();
}


const stop = async () =>
{
    const response = await fetch('/stop', fetchParameters);
    return await response.json();
}

const switchClipTables = async (button) =>
{
    if (currentlyDisplayedTable === 'tableShowClips')
    {
        listClipsAsTable(currentPlayList, 'P');
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


const getPlayLists = async () =>
{
    const response = await fetch(`/playlist`, fetchParameters);
    return await response.json();

}

const populateSelectControlWithPlayLists = async () =>
{
    const playLists = await getPlayLists();
    const selectPlaylists = document.getElementById('selectPlayLists');
    for (const playList of playLists)
    {
        const option = document.createElement('option');
        option.value = playList['playListId'];
        option.text = playList['playListName'];
        selectPlaylists.appendChild(option);
    }
}

const getClipsInPlayList = async (selectControl) =>
{
    const playListId = selectControl.value;
    const response = await fetch(`/playlist/${playListId}`, fetchParameters);
    const data = await response.json();
    return data;
}

const refreshClipList  = () =>
{
    getHyperDeckClips()
    .then((clipList =>
    {
        hyperDeckClipList = clipList;
        listClipsAsTable(clipList, 'H')
    }));
}

const addClipToPlayList = (clip) =>
{
    if (!currentPlayList.find(playListClip => playListClip.index === clip.index ))
    {
        currentPlayList.push(clip);
    }
    listClipsAsTable(hyperDeckClipList, 'H');
}

const addClipToPlayListOnServer = async (clip) =>
{
    const response = await fetch('/status', fetchParameters);
    const data = await response.json();
}

const removeClipFromPlayList = (clip) =>
{
    if (currentPlayList.find(playListClip => playListClip.index === clip.index ))
    {
        let updatedPlayList = [];
        for (let thisClip of currentPlayList)
        {
            if (thisClip.index !== clip.index)
                updatedPlayList.push(thisClip);
        }
        currentPlayList = updatedPlayList;
    }
    listClipsAsTable( currentPlayList, 'P');
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

        tdClipIndex.innerText = clip.hyperDeckClipIndex;
        tdClipName.innerText = clip.name;
        tdClipTimeCode.innerText = clip.timecode;
        tdClipDuration.innerText = clip.duration;


        const buttonAddRemoveClip = document.createElement('button');
        buttonAddRemoveClip.onclick = () => addClipToPlayList(clip);
        if (clipListType === "H")
        {
            const clipInPlaylistCount = currentPlayList.filter(playListClip => playListClip.hyperDeckClipIndex === clip.hyperDeckClipIndex ).length;
            buttonAddRemoveClip.innerText = `Add ${clipInPlaylistCount > 0 ? " again" : ""}`;
            buttonAddRemoveClip.onclick = () => addClipToPlayList(clip);
        }
        else
        {
            buttonAddRemoveClip.onclick = () => removeClipFromPlayList(clip);
            buttonAddRemoveClip.innerText = "Remove";
        }
        tdActions.appendChild(buttonAddRemoveClip);

        const buttonPlayNow = document.createElement('button');
        buttonPlayNow.onclick = () => playNow(clip.hyperDeckClipIndex, false);
        buttonPlayNow.innerText = "Play Now";

        tdActions.appendChild(buttonPlayNow);

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

const getCurrentPlayList = async () =>
{
    //Get current playlist
    currentPlayList = await getClipsInPlayList(document.getElementById('selectPlayLists'));
}


window.addEventListener('load',  () =>
{
    displayHyperDeckStatus()
        .then(() => getHyperDeckClips())
        .then((clipList =>
            {
                hyperDeckClipList = clipList;
                listClipsAsTable(clipList, 'H')
            }))
        .then(() => populateSelectControlWithPlayLists())
        .then(() => getCurrentPlayList());
})

setInterval(displayHyperDeckStatus, 500);
