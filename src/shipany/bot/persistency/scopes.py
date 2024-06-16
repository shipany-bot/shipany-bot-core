from enum import StrEnum


class Scope(StrEnum):
  """State scope.

  It is important to note that the state is stored in the concrete scope. The scope can be chat or user, or both.

  Chat scope is used to store the state for the current chat. The values stored in chat scope are available
  for all users in the chat. The values stored in chat scope are not available for other chats.

  User scope is used to store the state for the current user. The values stored in user scope are available
  for the current user across all chats. The values stored in user scope are not available for other users.

  Session store is used to store the state between the different steps of the conversation. They are available only
  for the current user and the current chat.

  """

  chat = "chat"
  user = "user"
