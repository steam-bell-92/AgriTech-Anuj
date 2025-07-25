// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('crop-form');
    const resultContainer = document.getElementById('result-container');
    const resultText = document.getElementById('result-text');
    const guideContainer = document.getElementById('guide-container');
    const guideTitle = document.getElementById('guide-title');
    const guideTimeline = document.getElementById('guide-timeline');
    const guideHowToPlant = document.getElementById('guide-how-to-plant');
    const guideFertilizer = document.getElementById('guide-fertilizer');
    const guideIdealRainfall = document.getElementById('guide-ideal-rainfall');
    const guidePostHarvest = document.getElementById('guide-post-harvest');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            const el = document.getElementsByName(key)[0];
            data[key] = el.type === 'number' ? parseFloat(value) : value;
        });

        displayLoading();

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: data }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const result = await response.json();
            
            if (result.crop && result.guide_json_string) {
                const guide = JSON.parse(result.guide_json_string);
                displayResultAndGuide(result.crop, guide);
            } else {
                displayError(result.error || "An unknown error occurred.");
            }

        } catch (error) {
            console.error("Error calling prediction API:", error);
            displayError("Could not connect to the server.");
        }
    });

    function displayLoading() {
        resultContainer.classList.remove('hidden');
        resultText.textContent = 'Curating your personalized crop guide...';
        guideContainer.classList.add('hidden');
    }

    function displayError(message) {
        resultContainer.classList.remove('hidden');
        resultText.textContent = message;
        guideContainer.classList.add('hidden');
    }

    // **NEW FUNCTION TO CONVERT MARKDOWN TO HTML**
    function formatAIResponse(text) {
        if (!text) return '';
        // Convert **bold** to <strong>bold</strong>
        let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Convert newlines to <br> tags
        formattedText = formattedText.replace(/\n/g, '<br>');
        return formattedText;
    }

    function displayResultAndGuide(cropName, guide) {
        resultContainer.classList.remove('hidden');
        resultText.textContent = cropName;

        guideTitle.textContent = guide.title;
        
        // **USE THE NEW FORMATTING FUNCTION AND .innerHTML**
        guideTimeline.innerHTML = formatAIResponse(guide.timeline);
        guideHowToPlant.innerHTML = formatAIResponse(guide.how_to_plant);
        guideFertilizer.innerHTML = formatAIResponse(guide.fertilizer);
        guideIdealRainfall.innerHTML = formatAIResponse(guide.ideal_rainfall);
        guidePostHarvest.innerHTML = formatAIResponse(guide.post_harvest);
        
        guideContainer.classList.remove('hidden');
    }
});