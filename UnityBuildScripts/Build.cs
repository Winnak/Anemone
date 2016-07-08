/// <copyright file="Build.cs">
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
    using UnityEditor;

    /// <summary>
    /// Contains all methods required by the build slaves of Anemone
    /// </summary>
    internal static class Build
    {
        /// <summary>
        /// Builds a debug build for windows to the <see cref="kDefaultBuildPath"/>
        /// </summary>
        [MenuItem("File/Anemone Build/Windows x86 (Debug)")]
        private static void WindowsDebug()
        {
            BuildUtility.BuildProject("windows-debug", BuildTarget.StandaloneWindows, (BuildOptions.AllowDebugging | BuildOptions.Development));
        }

        /// <summary>
        /// Builds a windows build to the <see cref="kDefaultBuildPath"/>
        /// </summary>
        [MenuItem("File/Anemone Build/Windows x86")]
        private static void Windows()
        {
            BuildUtility.BuildProject("windows", BuildTarget.StandaloneWindows, BuildOptions.None);
        }
    }
}
