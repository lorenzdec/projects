function deleteNote(noteId) {   // takes noteId and sends post request to delete-note endpoint
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href= "/"; // redirect to homepage, which refreshes page
    });
}