class MessageBlock extends React.Component {
    constructor(props) {
        super(props);
    }

    render = () => {
        return (
            <div className="message">
                <h4>{this.props.user}</h4>
                {this.props.content}
            </div>
        )
        
    }
}

class ChatForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {chatMessages: [], messageText: ''};
    }

    addMessage = (user, content) => {
        this.state.chatMessages.push({
            'user': user,
            'content': content
        });

        this.setState({
            ['chatMessages']: this.state.chatMessages
        });

        console.log(this.state.chatMessages);
    }

    componentDidMount = () => {
        globalThis.rltProto.addEventListener((data) => {
            
            if (data.event_type == "encrypted_message") {
                this.addMessage(
                    data.from_user_id,
                    Aes.Ctr.decrypt(data.enrypted_content, globalThis.private_key, 256)
                )
            }

        });
    }

    handleMessageText(event) {
        const textBoxValue = `${event.target.value}`;
        
        this.setState({
            ['messageText']: textBoxValue
        });
    }

    handleSubmit(event) {
        const messageText = this.state.messageText;

        try{

            rltProto.send({
                'method': 'send_message',
                'conversation_id': globalThis.conversation_id,
                'encrypted_message_content': Aes.Ctr.encrypt(messageText, globalThis.private_key, 256),
                'user_id': globalThis.user_id
            })

        } catch(e) {
            console.log(e);
        }

        event.preventDefault();
    }

    render = () => {
        
        return (
            <form onSubmit={this.handleSubmit.bind(this)}>
                <div className="chatBox">
                    Chat:
                    <div>
                        {this.state.chatMessages.map((message) => 
                            <MessageBlock user={message.user} content={message.content} />
                        )}
                    </div>
                </div>
                <label>
                    Message text: 
                    <input type="text" value={this.state.messageText} onChange={this.handleMessageText.bind(this)} />
                </label>
                <input type="submit" value="Connect" />
            </form>
        )
    }
}

class SettingsForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'STATE': 'FILLER'
        };
    
    }
    
    handleChange(event) {
        const target = event.target;
        const value = target.value;

        console.log(event);
        this.state['nameValue'] = value;
    }
    
    handleMembersChange(event) {
        const target = event.target;
        const value = target.value;

        console.log(event);
        this.state['membersValue'] = value;
    }

    handleCreateConversationValueChange(event) {
        console.log(event);
        const checked = event.target.checked;
        this.state['createConversationValue'] = checked;
    }
    
    handleSubmit(event) {
        const membersValue = `${this.state.membersValue}`;
        const create_conversation = this.state.createConversationValue;
        const your_user_id = this.state.nameValue;

        try{
            globalThis.rltProto.connect(this.state.nameValue, function() {

                globalThis.user_id = your_user_id;

                if (create_conversation){
                    try {
                        globalThis.rltProto.send({
                            'method': 'create_conversation',
                            'members': membersValue.split(',')
                        });
                    }
                    catch (e) {
                        console.log(membersValue);
                        console.log(e);
                    }
                }
                
            })
        }
        catch (e) {
            console.log(e);
        }
        

        try {
            globalThis.rltProto.listen();
        }
        catch (e) {
            console.log(e);
        }
        

        globalThis.rltProto.addEventListener((data) => {

            console.log(data)
    
            if (data.event_type == "create_private_conversation") {
                globalThis.conversation_id = data.conversation_id;
                globalThis.private_key = data.private_key;
            }

        });
        
        
        event.preventDefault();
    }

    render = () => {
        return (
            <form onSubmit={this.handleSubmit.bind(this)}>
                <label>
                    Temporary Name:
                    <input type="text" value={this.state.nameValue} onChange={this.handleChange.bind(this)} />
                </label>

                <label>
                    Create conversation: 
                    <input type="checkbox" value={this.state.createConversationValue} onChange={this.handleCreateConversationValueChange.bind(this)} />
                </label>

                <label>
                    Members (separate by comma):
                    <input type="text" value={this.state.membersValue} onChange={this.handleMembersChange.bind(this)} />
                </label>
                <input type="submit" value="Connect" />
            </form>
        )
    }
}

class Index extends React.Component {

    render = () => {

        return (
            <div className="content">
                <h2>Crypto messaging test</h2>
                <p>This example shows how safe you can talk.</p>
                <SettingsForm />
                <ChatForm />
            </div>
        )
    }

}

globalThis.rltProto = new RLTProto();

const root = ReactDOM.createRoot(document.querySelector("#root"));
root.render(<Index />);