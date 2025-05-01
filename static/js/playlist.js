// static/playlist.js
function openNoteModal() {
    const selected = document.querySelector('input[name="song_id"]:checked');
    if (!selected) {
        alert("Please select a song first.");
        return;
    }
    document.getElementById('noteModal').style.display = 'block';
}

function submitWithNote() {
    const note = document.getElementById('noteInput').value;
    const hiddenNote = document.getElementById('user_note');
    hiddenNote.style.display = 'block';
    hiddenNote.value = note;
    document.getElementById('add-song-form').submit();
}

function submitWithoutNote() {
    document.getElementById('noteModal').style.display = 'none';
    document.getElementById('add-song-form').submit();
}

document.addEventListener("DOMContentLoaded", function() {
    // Make the entire song row clickable
    const songRows = document.querySelectorAll(".song-row");
    songRows.forEach(function(row) {
        row.addEventListener("click", function() {
            const songUrl = row.getAttribute("data-song-url");
            if (songUrl) {
                window.location.href = songUrl;
            }
        });
    });

    // Handle "Add" button click on albums
    const addButtons = document.querySelectorAll(".add-button");
    addButtons.forEach(function(button) {
        button.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent parent click
            const addUrl = button.getAttribute("data-add-url");
            if (addUrl) {
                window.location.href = addUrl;
            }
        });
    });

    // Optional: Smooth scroll to sections
    const links = document.querySelectorAll("a[href^='#']");
    links.forEach(function(link) {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: "smooth"
                });
            }
        });
    });
});
