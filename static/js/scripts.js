function redirectToSearch() {
  setTimeout(function() {
    window.location.href = "{{ url_for('templates.search') }}";
  }, 7000); // 5초 (5000 밀리초)
}