const getClips = async () =>
{
    const response = await fetch('/getclips');
    const data = await response.json();
    return data
}

console.log(getClips());