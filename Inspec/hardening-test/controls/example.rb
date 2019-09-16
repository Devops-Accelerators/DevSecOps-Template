require_controls 'linux-baseline' do
  control 'os-01'
end

require_controls 'ssh-baseline' do
  control 'ssh-01'
  control 'ssh-03'
end
