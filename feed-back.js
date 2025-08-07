document.addEventListener('DOMContentLoaded', function() {
  const feedbackForm = document.getElementById('feedbackForm');
  const thankYouMessage = document.getElementById('thankYouMessage');
  const feedbackTitle = document.querySelector('.feedback-title');
  const allFeedbacksSection = document.getElementById('allFeedbacks');
  const viewFeedbacksBtn = document.getElementById('viewFeedbacks');
  const feedbacksList = document.getElementById('feedbacksList');

  // Initialize storage if it doesn't exist
  if (!localStorage.getItem('agritechFeedbacks')) {
    localStorage.setItem('agritechFeedbacks', JSON.stringify([]));
  }

  feedbackForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const feedbackData = {
      name: document.getElementById('name').value.trim(),
      email: document.getElementById('email').value.trim() || 'Not provided',
      feedback: document.getElementById('feedback').value.trim(),
      date: new Date().toLocaleString()
    };

    // Save to local storage
    const allFeedbacks = JSON.parse(localStorage.getItem('agritechFeedbacks'));
    allFeedbacks.push(feedbackData);
    localStorage.setItem('agritechFeedbacks', JSON.stringify(allFeedbacks));

    // Show thank you message
    feedbackForm.classList.add('hidden');
    feedbackTitle.classList.add('hidden');
    thankYouMessage.classList.remove('hidden');
    feedbackForm.reset();
  });

  // View all feedbacks
  viewFeedbacksBtn.addEventListener('click', function() {
    thankYouMessage.classList.add('hidden');
    displayAllFeedbacks();
  });

  // Email validation
  const emailInput = document.getElementById('email');
  emailInput.addEventListener('blur', function() {
    if (emailInput.value && !validateEmail(emailInput.value)) {
      alert('Please enter a valid email address');
      emailInput.focus();
    }
  });

  // Display all feedbacks
  function displayAllFeedbacks() {
    const allFeedbacks = JSON.parse(localStorage.getItem('agritechFeedbacks'));
    allFeedbacksSection.classList.remove('hidden');
    
    if (allFeedbacks.length === 0) {
      feedbacksList.innerHTML = '<p>No feedback submissions yet.</p>';
      return;
    }

    feedbacksList.innerHTML = allFeedbacks.map((fb, index) => `
      <div class="feedback-item">
        <h4>${fb.name}</h4>
        ${fb.email !== 'Not provided' ? `<p>Email: ${fb.email}</p>` : ''}
        <p>${fb.feedback}</p>
        <div class="feedback-meta">
          Submission #${index + 1} • ${fb.date}
        </div>
      </div>
    `).join('');
  }
});

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}