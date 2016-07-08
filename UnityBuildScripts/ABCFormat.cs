/// <copyright file="ABCFormat.cs">
/// MIT License
///
/// Copyright(c) 2016 Erik Høyrup Jørgensen
///
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
///
/// The above copyright notice and this permission notice shall be included in all
/// copies or substantial portions of the Software.
///
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
/// SOFTWARE.
/// </copyright>
/// <author>Erik Høyrup Jørgensen</author>
/// <date>03/25/2016 18:15</date>
/// <summary>Class for build methods required by Unity for the Anemone project.</summary>

/// <summary>
/// Part of the Anemone CI (https://github.com/winnak/anemone)
/// </summary>
namespace Anemone
{
    /// <summary>
    /// Anemone Build Configuration-format node. Use <see cref="ParseFile(string)"/> to create.
    /// </summary>
    internal class ABCFormat
    {
        /// <summary>
        /// Parses an .abc file.
        /// </summary>
        /// <param name="path">path to the .abc-file</param>
        /// <returns>The root node in the ABC-file format structure</returns>
        internal static ABCFormat ParseFile(string path)
        {
            if (!System.IO.File.Exists(path)) { return NullNode; }

            string[] lines = System.IO.File.ReadAllLines(path);
            ABCFormat root = new ABCFormat("root");
            ABCFormat currentNode = root;

            for (int i = 0; i < lines.Length; i++)
            {
                string line = lines[i];
                if (line.IndexOf('#') != -1) { line = line.Split('#')[0]; }
                if (line.Trim() == string.Empty) { continue; }
                if (line[0] != '\t') { currentNode = root; }

                for (int c = 0; c < line.Length; c++)
                {
                    if (line[c] == '=')
                    {
                        string key = line.Substring(0, c).Trim();
                        if (key.Length == 0) { break; }
                        string value = line.Substring(c + 1, line.Length - c - 1).Trim();
                        currentNode.Set(key, value);
                        break;
                    }
                    else if (line[c] == ':')
                    {
                        string key = line.Substring(0, c).Trim();
                        if (key.Length == 0) { break; }
                        currentNode = new ABCFormat(key, currentNode);
                        break;
                    }
                }
            }

            return root;
        }

        public static readonly ABCFormat NullNode = new ABCFormat(string.Empty);
        private string m_Key;
        private ABCFormat m_Parent;
        private System.Collections.Generic.Dictionary<string, string> m_Values = new System.Collections.Generic.Dictionary<string, string>();
        private System.Collections.Generic.Dictionary<string, ABCFormat> m_Nodes = new System.Collections.Generic.Dictionary<string, ABCFormat>();

        /// <summary>
        /// Gets or sets the subnodes of this node
        /// </summary>
        /// <param name="key">Subnodes key.</param>
        /// <returns>The subnode.</returns>
        internal ABCFormat this[string key]
        {
            get
            {
                ABCFormat value;
                if (!m_Nodes.TryGetValue(key, out value)) { value = NullNode; }
                return value;
            }
            set
            {
                if (m_Nodes.ContainsKey(key)) { m_Nodes[key] = value; }
                else { m_Nodes.Add(key, value); }
                value.m_Parent = this;
            }
        }

        /// <summary>
        /// Private constructer for an ABC node. Use <see cref="ParseFile(string)"/> instead.
        /// </summary>
        /// <param name="key">This nodes key.</param>
        /// <param name="parent">The parent of this node.</param>
        private ABCFormat(string key, ABCFormat parent = null)
        {
            m_Key = key;
            m_Parent = parent;
            if (parent != null) { parent[key] = this; }
        }

        /// <summary>
        /// Gets the value of this configuration setting (or the default)
        /// </summary>
        /// <param name="key">Setting key.</param>
        /// <returns>Returns value of setting.</returns>
        internal string Get(string key)
        {
            string value = null;
            if (!m_Values.TryGetValue(key, out value)) { if (m_Parent != null) { return m_Parent.Get(key); } }
            if (value == null) { value = string.Empty; }
            return value;
        }

        /// <summary>
        /// Sets a setting of this node
        /// </summary>
        /// <param name="key">Setting key.</param>
        /// <param name="value">Setting value.</param>
        internal void Set(string key, string value)
        {
            if (m_Values.ContainsKey(key)) { m_Values[key] = value; }
            else { m_Values.Add(key, value); }
        }

        /// <summary>
        /// Returns a user friendly string representing this object
        /// </summary>
        /// <returns>This key, followed by the amount of settings stored in this node, followed by the amount of configurations beneath this node.</returns>
        public override string ToString() { return m_Key; }
    }
}
