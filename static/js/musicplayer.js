document.getElementById('midiPlayer').addEventListener('play', function() {
    // Web MIDI API code
    if (navigator.requestMIDIAccess) {
        navigator.requestMIDIAccess().then(onMIDISuccess, onMIDIFailure);
    } else {
        console.log("Web MIDI API not supported by this browser.");
    }

    function onMIDISuccess(midiAccess) {
        var inputs = midiAccess.inputs.values();
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            input.value.onmidimessage = getMIDIMessage;
        }
    }

    function onMIDIFailure(error) {
        console.log("Failed to access MIDI devices.", error);
    }

    function getMIDIMessage(message) {
        // Handle MIDI messages if needed
    }
});