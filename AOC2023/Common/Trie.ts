export class TrieNode {
    public children: Map<string, TrieNode>

    constructor(children: Map<string, TrieNode> = new Map(), public isWordEnd: boolean = false) {
        this.children = children;
    }
}

export class Trie {
    private root: TrieNode;

    constructor() {
        this.root = new TrieNode();
    }

    public insert(word: string): void {
        let node: TrieNode = this.root;
        for (let i = 0; i < word.length; i++) {
            const char = word[i];
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char) as TrieNode;
        }
        node.isWordEnd = true;
    }

    public search(word: string): boolean {
        let node: TrieNode = this.root;
        for (let i = 0; i < word.length; i++) {
            const char = word[i];
            if (!node.children.has(char)) {
                return false;
            }
            node = node.children.get(char) as TrieNode;
        }
        return node.isWordEnd;
    }

    public startsWith(prefix: string): boolean {
        let node: TrieNode = this.root;
        for (let i = 0; i < prefix.length; i++) {
            const char = prefix[i];
            if (!node.children.has(char)) {
                return false;
            }
            node = node.children.get(char) as TrieNode;
        }
        return true;
    }
}