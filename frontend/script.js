async function getValue() {
    var inputElement = document.getElementById('myIn');
    var inputValue = inputElement.value;
    document.getElementById("output").innerText = "Generating Notes... This May Take Few Moments";
    const apiUrl = 'https://notegen.gamick.eu.org/yt?url=';
    const apiUrl2 = '&language=';
    const lang = document.getElementById('lang').value;

    try {
        const response = await fetch(apiUrl + encodeURIComponent(inputValue) + apiUrl2 + lang); // Encode the URL parameter
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const responseText = await response.text(); // Read the response body once
        var OUTPUT = responseText;
        // Convert Markdown-like text to HTML
        const html = parseMarkdown(responseText);

        // Update the DOM with the formatted HTML
        document.getElementById("output").innerHTML = html;

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("output").innerText = "An error occurred. Please try again.";
    }
}

function parseMarkdown(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
        .replace(/(\r\n|\n|\r)/gm, '<br>') // Newlines to <br>
        .replace(/^(#+) (.*)$/gm, '<h$1>$2</h$1>') // Headers
        .replace(/([^\s]+)\n=+/g, '<h1>$1</h1>') // H1 headers
        .replace(/([^\s]+)\n-+/g, '<h2>$1</h2>') // H2 headers
        .replace(/!?\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>') // Links
        .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1">') // Images
        .replace(/~~(.*?)~~/g, '<del>$1</del>') // Strikethrough
        .replace(/__(.*?)__/g, '<u>$1</u>') // Underline
        .replace(/`(.*?)`/g, '<code>$1</code>') // Code
        .replace(/^(>+) (.*)$/gm, '<blockquote>$2</blockquote>') // Blockquotes
        .replace(/^-{3,}$/gm, '<hr>') // Horizontal rule
        .replace(/<p><br><\/p>/g, '<br>'); // Remove empty paragraphs
}

document.getElementById('myIn').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        getValue();
    }
});

async function downloadPDF() {
    var inputElement = document.getElementById('myIn');
    var inputValue = inputElement.value;
    document.getElementById("output").innerText = "Generating PDF... This May Take a Few Moments";
    const apiUrl = 'https://notegen.gamick.eu.org/download_pdf?url=';

    try {
        const response = await fetch(apiUrl + encodeURIComponent(inputValue)); // Encode the URL parameter
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Create a Blob from the response
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'note.pdf'; // Set the default file name
        link.click();
        
        // Optional: Clean up the URL object
        window.URL.revokeObjectURL(link.href);

        document.getElementById("output").innerText = "Download started. If the download does not start automatically, please check your browser's download folder.";

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("output").innerText = "An error occurred. Please try again.";
    }
}
