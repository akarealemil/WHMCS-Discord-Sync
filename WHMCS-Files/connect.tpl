{if $status == 'success'}
<div class="alert alert-success" role="alert">
  <h4 class="alert-heading">Success</h4>
  <p>You have successfully connected your discord and whmcs account!</p>
  <hr>
  <p class="mb-0">You can now close this page.</p>
</div>
{else if $status == 'connected'}
<div class="alert alert-warning" role="alert">
  <p><strong>Oh no!</strong> You are already connected.</p>
</div>
{else if $status == 'debug'}
<div class="alert alert-warning" role="alert">
  <h4 class="alert-heading">Debug</h4>
  <p>Debug Message: ({$debug})</p>
</div>
{else}
<div class="alert alert-danger" role="alert">
  <h4 class="alert-heading">An Error Occurred</h4>
  <p>An error occurred while trying to sync your discord & whmcs account.</p>
  <hr>
  <p class="mb-0">Please report this to a support member on discord</p>
</div>
{/if}