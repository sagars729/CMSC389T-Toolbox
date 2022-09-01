const USERNAME_FIELD = 'Github Username'; //must match the form
const STUDENTS_TEAM = 'Students';  //should not change
const ORGANIZATION = ''; //e.x. cmsc389T-fall22
const GITHUB_TOKEN = ''; //must have admin rights on your org

const FETCH_HEADERS = {
  'Accept': 'application/vnd.github+json',
  'Authorization': `Bearer ${GITHUB_TOKEN}`
}

async function add_student() {
  // get the last submitted username
  const form = FormApp.getActiveForm();
  const lastResponse = form.getResponses().pop().getItemResponses();
  const usernameIndex = lastResponse.findIndex(
    (item) => item.getItem().getTitle() == USERNAME_FIELD)
  const username = lastResponse[usernameIndex].getResponse();

  // get user id
  var response = await UrlFetchApp.fetch(
    `https://api.github.com/users/${username}`, 
    {'headers': FETCH_HEADERS}
  )
  const userid = JSON.parse(response)['id']

  // get team id
  var response = await UrlFetchApp.fetch(
    `https://api.github.com/orgs/${ORGANIZATION}/teams/${STUDENTS_TEAM}`,
    {'headers': FETCH_HEADERS}
  )
  const teamid = JSON.parse(response)['id']

  // send an invite
  var response = await UrlFetchApp.fetch(
    `https://api.github.com/orgs/${ORGANIZATION}/invitations`,
    {
      'method': 'post',
      'headers': FETCH_HEADERS,
      'payload': JSON.stringify({
        "invitee_id": userid,
        "role":"direct_member",
        "team_ids":[teamid]
      }),
      muteHttpExceptions: true
    }
  )

  // add to logs to help debug if needed
  console.log(response.getContentText())
}

