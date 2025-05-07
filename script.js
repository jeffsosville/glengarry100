const supabase = supabase.createClient('https://rxbaimgjakefhxsaksdl.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4YmFpbWdqYWtlZmh4c2Frc2RsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY2MjY0NDksImV4cCI6MjA2MjIwMjQ0OX0.k7dgerrSld8mZN3wvJIZkISVN1x4FWI-SyOVkEJF8lU');

async function loadLeaderboard() {
  const { data, error } = await supabase
    .from('brokers')
    .select('*')
    .order('listings_count', { ascending: false })
    .limit(100);

  if (error) {
    console.error(error);
    document.getElementById('leaderboard').innerHTML = "<li>Failed to load data</li>";
    return;
  }

  const leaderboard = document.getElementById('leaderboard');

  data.forEach((row, index) => {
    leaderboard.innerHTML += `
      <li>
        <span class="rank">${index + 1}.</span>
        <strong>${row.name}</strong>
        <span class="company">${row.companyName}</span>
        <span class="listings">${row.listings_count} listings</span>
        ${row.nicheTag ? `<span class="badge">${row.nicheTag}</span>` : ''}
        <a href="${row.listings_url}" target="_blank">[View]</a>
      </li>`;
  });
}

loadLeaderboard();
