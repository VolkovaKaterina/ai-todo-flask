function openEditModal(taskId) {
    document.getElementById(`edit-modal-${taskId}`).classList.add("is-active");
  }
  function closeEditModal(taskId) {
    document.getElementById(`edit-modal-${taskId}`).classList.remove("is-active");
  }
  